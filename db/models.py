from enum import Enum

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BirthGenger(Enum):
    female = 'female'
    male = 'male'


class ImportId(Base):
    __tablename__ = 'import_ids'
    id = sa.Column(sa.Integer, primary_key=True)


import_id_table = ImportId.__table__


class Citizen(Base):
    __tablename__ = 'citizens'

    id = sa.Column(sa.Integer, primary_key=True)
    import_id = sa.Column(sa.Integer, nullable=False)
    citizen_id = sa.Column(sa.Integer, nullable=False)
    town = sa.Column(sa.String(256), nullable=False)
    street = sa.Column(sa.String(256), nullable=False)
    building = sa.Column(sa.String(256), nullable=False)
    apartment = sa.Column(sa.Integer, nullable=False)
    name = sa.Column(sa.String(256), nullable=False)
    birth_date = sa.Column(sa.DateTime, nullable=False)
    gender = sa.Column(sa.Enum(BirthGenger), nullable=False)


citizen_table = Citizen.__table__


class Relative(Base):
    __tablename__ = 'relatives'

    id = sa.Column(sa.Integer, primary_key=True)
    import_id = sa.Column(sa.Integer, nullable=False)
    citizen_id = sa.Column(sa.Integer, nullable=False)
    relative_id = sa.Column(sa.Integer, nullable=False)


relative_table = Relative.__table__
