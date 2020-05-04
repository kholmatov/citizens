from datetime import datetime

import marshmallow

from utils.request_schema import CitizenImport


def validate_import_citizens(data):
    relatives = {}
    schema = CitizenImport(check_all_fields=True)
    all_citizens = []
    for elem in data:
        try:
            result = schema.load(elem)
        except marshmallow.exceptions.ValidationError as e:
            print(e)
            return [], str(e)

        if result['citizen_id'] in set(result['relatives']):
            return [], 'Citizen {} contains in relatives'.format(
                result['citizen_id']
            )

        relatives[result['citizen_id']] = set(result['relatives'])
        all_citizens.append(result)

    for citizen_id, relative_ids in relatives.items():
        for relative in relative_ids:
            if relative not in relatives:
                return (
                    [],
                    'Relative {} should contain in import '
                    'as citizen also'.format(relative)
                )
            if citizen_id not in relatives[relative]:
                return (
                    [],
                    'Citizen {} should be in {} relatives'.format(
                        citizen_id, relative
                    )
                )
    return all_citizens, None


def validate_patch_citizens(data, citizen_id):

    schema = CitizenImport(check_all_fields=False)
    try:
        citizen_diff = schema.load(data)
    except marshmallow.exceptions.ValidationError as e:
        return {}, str(e)

    if not citizen_diff:
        return {}, 'Diff should not be empty'

    if 'citizen_id' in citizen_diff:
        return {}, 'Citizen id {} contains in diff'.format(
            schema['citizen_id']
        )

    if (
            'relatives' in citizen_diff and
            citizen_id in set(citizen_diff['relatives'])
    ):
        return {}, 'Relatives in citizen_diff and citizen_id in relatives'

    return citizen_diff, None
