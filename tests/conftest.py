import json

import pytest

from db import create_engine
from db.models import Base


@pytest.fixture
def citizens_data():
    with open('tests/data/citizens.json') as f:
        return json.load(f)['citizens']


@pytest.fixture
def create_db():
    engine = create_engine()
    Base.metadata.create_all(engine)
