from operator import itemgetter

import pytest
from flask import url_for


def test_get(client, citizens_import_id, citizens_data):
    resp = client.get(
        url_for('imports.get_import_citizens', import_id=citizens_import_id)
    )

    assert resp.status_code == 200

    results = resp.json['data']
    assert len(results) == len(citizens_data)

    for got, expected in zip(
            sorted(results, key=itemgetter('citizen_id')),
            sorted(citizens_data, key=itemgetter('citizen_id'))
    ):
        assert got == expected


def test_get_not_exists(client, citizens_import_id, citizens_data):
    import_id = citizens_import_id + 1  # Doesn't exists
    resp = client.get(
        url_for('imports.get_import_citizens', import_id=import_id)
    )

    assert resp.status_code == 200


@pytest.mark.parametrize(
    ('import_id'), [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    ]
)
def test_get_no_data(import_id, client):
    resp = client.get(
        url_for('imports.get_import_citizens', import_id=import_id)
    )

    assert resp.status_code == 200


@pytest.mark.parametrize(
    ('import_id, status'), [
        (1, 200),
        (-1, 404),
        ('ololo', 404),
        ('10', 200),
        ('', 404),
    ]
)
def test_get_import_id(import_id, status, client):
    resp = client.get(
        f'imports/{import_id}/citizens'
    )

    assert resp.status_code == status
