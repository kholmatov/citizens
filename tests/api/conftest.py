import pytest

from citizens.app import create_app
from citizens.handlers.imports import insert_citizens
from utils.validate import validate_import_citizens


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def citizens_import_id(citizens_data, create_db):
    all_citizens, error = validate_import_citizens(citizens_data)
    if error is not None:
        raise Exception(error)
    import_id = insert_citizens(all_citizens)
    return import_id
