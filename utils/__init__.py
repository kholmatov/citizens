import sqlalchemy as sa

from utils.request_schema import CitizenImport
from db.models import relative_table


def citizen_record_obj_to_dict(conn, import_id, citizen_rec):
    d = dict(citizen_rec)
    d['gender'] = d['gender'].value
    d['birth_date'] = d['birth_date'].strftime('%d.%m.%Y')
    d['relatives'] = get_relatives_list(conn, import_id, citizen_rec.citizen_id)
    del d['id']
    del d['import_id']
    return d


def get_relatives_list(conn, import_id, citizen_id):
    s = sa.select(
        [relative_table.c.citizen_id, relative_table.c.relative_id]
    ).where(
        sa.and_(
            relative_table.c.import_id == import_id,
            sa.or_(
                relative_table.c.citizen_id == citizen_id,
                relative_table.c.relative_id == citizen_id
            )
        )
    )
    rows = conn.execute(s)
    results = []
    for r in rows:
        if r.citizen_id != citizen_id:
            results.append(r.citizen_id)
        else:
            results.append(r.relative_id)
    return results
