import os

import sqlalchemy as sa


def create_engine():
    engine = sa.create_engine(os.environ['DATABASE_URL'], echo=True)
    return engine
