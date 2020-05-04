import datetime

from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import OneOf

from db.models import BirthGenger


def _validate_str(s):
    return s and len(s) <= 256


def _validate_str_isalnum(s):
    return _validate_str(s) and any(map(str.isalnum, s))


class CitizenImport(Schema):
    def __init__(self, check_all_fields=False):
        super().__init__()
        self.do_check_all_fields = check_all_fields

    @validates_schema(pass_original=True)
    def check_all_fields(self, data, original_data, **kwargs):
        if self.do_check_all_fields and set(original_data) != set(self.fields):
            raise ValidationError('All fields should be passed')

    citizen_id = fields.Integer(validate=lambda x: x >= 0)
    town = fields.String(validate=_validate_str_isalnum)
    street = fields.String(validate=_validate_str_isalnum)
    building = fields.String(validate=_validate_str_isalnum)
    name = fields.String(validate=_validate_str)
    apartment = fields.Integer(validate=lambda x: x >= 0)
    birth_date = fields.Date(
        format='%d.%m.%Y', validate=lambda d: d < datetime.date.today()
    )
    gender = fields.String(validate=OneOf(
        list(gender.value for gender in BirthGenger.__members__.values())
    ))
    relatives = fields.List(
        fields.Integer(validate=lambda x: x >= 0),
        validate=lambda x: len(set(x)) == len(x)
    )
