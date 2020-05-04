from operator import itemgetter

import pytest
from flask import url_for


def test_post(client, citizens_data):
    resp = client.post(
        url_for('imports.import_citizens'),
        json={'citizens': citizens_data}
    )
    assert resp.status_code == 201
    import_id = resp.json['data']['import_id']

    got = client.get(
        url_for('imports.get_import_citizens', import_id=import_id)
    )
    assert got.status_code == 200

    results = got.json['data']
    assert len(results) == len(citizens_data)

    for got, expected in zip(
            sorted(results, key=itemgetter('citizen_id')),
            sorted(citizens_data, key=itemgetter('citizen_id'))
    ):
        assert got == expected


def test_post_many(client, citizens_data):
    import_ids = []
    for i in range(10):
        resp = client.post(
            url_for('imports.import_citizens'),
            json={'citizens': citizens_data}
        )
        assert resp.status_code == 201
        import_ids.append(resp.json['data']['import_id'])

    for i in import_ids:
        got = client.get(
            url_for('imports.get_import_citizens', import_id=i)
        )
        assert got.status_code == 200

        results = got.json['data']
        assert len(results) == len(citizens_data)

        for got, expected in zip(
                sorted(results, key=itemgetter('citizen_id')),
                sorted(citizens_data, key=itemgetter('citizen_id'))
        ):
            assert got == expected


@pytest.mark.parametrize(
    ('data, status'), [
        ({}, 400),
        ({'citizens': []}, 400),
        ({'citizens': ['ololo']}, 400),
        ({
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Амурск",
                    "street": "ул. Крестьянская",
                    "building": "32",
                    "apartment": 29,
                    "name": "Третьяков Богдан Харлампович",
                    "birth_date": "02.05.1949",
                    "gender": "male",
                    "relatives": []
                },
                {
                    "citizen_id": 2,
                    "town": "Ивдель",
                    "street": "ул. Войкова",
                    "building": "95",
                    "apartment": 14,
                    "name": "Воронцова Нинель Алексеевна",
                    "birth_date": "16.08.1969",
                    "gender": "female",
                    "relatives": [7]
                }
            ]
        }, 400),
        ({
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Амурск",
                    "street": "ул. Крестьянская",
                    "building": "32",
                    "apartment": 29,
                    "name": "Третьяков Богдан Харлампович",
                    "birth_date": "02.05.1949",
                    "gender": "male",
                    "relatives": []
                },
                {
                    "citizen_id": 2,
                    "town": "Ивдель",
                    "street": "ул. Войкова",
                    "building": "95",
                    "apartment": 14,
                    "name": "Воронцова Нинель Алексеевна",
                    "birth_date": "16.08.1969",
                    "gender": "female",
                    "relatives": []
                }
            ]
        }, 201),
        ({
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Амурск",
                    "street": "ул. Крестьянская",
                    "building": "32",
                    "apartment": 29,
                    "name": "Третьяков Богдан Харлампович",
                    "birth_date": "02.05.1949",
                    "gender": "male",
                    "relatives": [2]
                },
                {
                    "citizen_id": 2,
                    "town": "Ивдель",
                    "street": "ул. Войкова",
                    "building": "95",
                    "apartment": 14,
                    "name": "Воронцова Нинель Алексеевна",
                    "birth_date": "16.08.1969",
                    "gender": "female",
                    "relatives": []
                }
            ]
        }, 400),
        ({
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "Амурск",
                    "street": "ул. Крестьянская",
                    "building": "32",
                    "apartment": 29,
                    "name": "Третьяков Богдан Харлампович",
                    "birth_date": "02.05.1949",
                    "gender": "male",
                    "relatives": [2]
                },
                {
                    "citizen_id": 2,
                    "town": "Ивдель",
                    "street": "ул. Войкова",
                    "building": "95",
                    "apartment": 14,
                    "name": "Воронцова Нинель Алексеевна",
                    "birth_date": "16.08.1969",
                    "gender": "female",
                    "relatives": [1]
                }
            ]
        }, 201),

    ]
)
def test_post_failes(data, status, client):
    resp = client.post(
        url_for('imports.import_citizens'),
        json=data
    )
    assert resp.status_code == status
