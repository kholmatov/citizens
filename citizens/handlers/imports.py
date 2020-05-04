import itertools
import json

from werkzeug.exceptions import BadRequest
from flask import Blueprint, request, Response
from sqlalchemy import and_, or_

from db.models import (
    import_id_table, citizen_table, relative_table
)
from db import create_engine
from utils import citizen_record_obj_to_dict
from utils.validate import validate_import_citizens, validate_patch_citizens
from utils import get_relatives_list

imports = Blueprint('imports', __name__)


@imports.route('/<int:import_id>/citizens', methods=['GET'])
def get_import_citizens(import_id):
    with create_engine().connect() as conn:
        with conn.begin():
            s = citizen_table.select().where(
                citizen_table.c.import_id == import_id
            )
            rows = conn.execute(s)
            result = []
            for citizen in rows:
                result.append(
                    citizen_record_obj_to_dict(conn, import_id, citizen)
                )
    return Response(
        json.dumps({'data': result}),
        status=200, mimetype='application/json'
    )


@imports.route('/', methods=['POST'])
def import_citizens():
    data = request.get_json(force=True)
    if 'citizens' not in data:
        raise BadRequest('Data doesn\'t contain `citizens` field')
    data = data['citizens']
    all_citizens, error = validate_import_citizens(data)
    if error is not None:
        raise BadRequest(error)
    if not all_citizens:
        raise BadRequest('Not found citizens to insert')
    import_id = insert_citizens(all_citizens)

    return Response(
        json.dumps({'data': {'import_id': import_id}}),
        status=201, mimetype='application/json'
    )


def insert_citizens(all_citizens):
    append_to_relatives = itertools.chain.from_iterable(
        (
            (citizen['citizen_id'], relative)
            for relative in citizen['relatives']
            if citizen['citizen_id'] < relative
        ) for citizen in all_citizens
    )

    with create_engine().connect() as conn:
        with conn.begin():

            import_id = conn.execute(
                import_id_table.insert()
            ).inserted_primary_key[0]

            to_insert_to_relatives = [
                {
                    'import_id': import_id,
                    'citizen_id': citizen,
                    'relative_id': relative
                } for citizen, relative in append_to_relatives
            ]

            to_insert_to_citizens = []
            for row in all_citizens:
                to_insert_to_citizens.append({
                    'import_id': import_id,
                    'apartment': row['apartment'],
                    'birth_date': row['birth_date'],
                    'building': row['building'],
                    'citizen_id': row['citizen_id'],
                    'gender': row['gender'],
                    'name': row['name'],
                    'street': row['street'],
                    'town': row['town'],
                })

            conn.execute(citizen_table.insert(), *to_insert_to_citizens)
            if to_insert_to_relatives:
                conn.execute(relative_table.insert(), *to_insert_to_relatives)

    return import_id


def get_citizen_record(conn, import_id, citizen_id):
    citizen_record_q = citizen_table.select().where(
        and_(
            citizen_table.c.import_id == import_id,
            citizen_table.c.citizen_id == citizen_id
        )
    )
    rows = conn.execute(citizen_record_q)
    return rows.fetchone()


def update_relatives(conn, import_id, citizen_id, relatives_list):
    new_relatives_set = set(relatives_list)
    curr_relatives_set = set(get_relatives_list(conn, import_id, citizen_id))
    deleted = list(curr_relatives_set - new_relatives_set)
    if deleted:
        del_rel_q = relative_table.delete().where(
            and_(
                relative_table.c.import_id == import_id,
                or_(
                    and_(
                        relative_table.c.citizen_id == citizen_id,
                        relative_table.c.relative_id.in_(deleted)
                    ),
                    and_(
                        relative_table.c.relative_id == citizen_id,
                        relative_table.c.citizen_id.in_(deleted)
                    )
                )
            )
        )
        conn.execute(del_rel_q)
    added_rel_tuples = [
        {'import_id': import_id, 'citizen_id': min(citizen_id, new_rel),
         'relative_id': max(citizen_id, new_rel)}
        for new_rel in (new_relatives_set - curr_relatives_set)
    ]
    if added_rel_tuples:
        conn.execute(relative_table.insert(), *added_rel_tuples)


@imports.route('/<int:import_id>/citizens/<int:citizen_id>', methods=['PATCH'])
def patch_citizen(import_id, citizen_id):
    data = request.get_json(force=True)
    citizen_diff, error = validate_patch_citizens(data, citizen_id)
    if error:
        print(error)
        raise BadRequest(error)

    with create_engine().connect() as conn:
        with conn.begin():
            citizen_record = get_citizen_record(conn, import_id, citizen_id)
            if citizen_record is None:
                raise BadRequest(
                    '{}, {} import_id, citizen_id pair is incorrect'.format(
                        import_id, citizen_id
                    )
                )
            relatives_new_list = citizen_diff.pop('relatives', None)
            for field, field_value in list(citizen_diff.items()):
                if citizen_record[field] == field_value:
                    del citizen_diff[field]
            if citizen_diff:
                update_q = citizen_table.update().where(
                    and_(
                        citizen_table.c.import_id == import_id,
                        citizen_table.c.citizen_id == citizen_id
                    )
                ).values(**citizen_diff)
                conn.execute(update_q)

            if relatives_new_list is not None:
                update_relatives(
                    conn, import_id, citizen_id, relatives_new_list
                )

            citizen_new_obj = conn.execute(citizen_table.select().where(
                and_(
                    citizen_table.c.import_id == import_id,
                    citizen_table.c.citizen_id == citizen_id
                )
            )).fetchone()
            return Response(
                json.dumps(
                    {
                        'data': citizen_record_obj_to_dict(
                            conn, import_id, citizen_new_obj
                        )
                    }
                ),
                status=200, mimetype='application/json'
            )
