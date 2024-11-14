from unittest.mock import patch

from routes.unit import units_blueprint
from tests.conftest import mock_db_response


# Test get_all_units endpoint
@patch("routes.unit.get_db_connection")
def test_get_all_units(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {"id": 1, "name": "Swordsman", "attack": 10},
            {"id": 2, "name": "Archer", "attack": 8},
        ],
    )

    response = client(units_blueprint).get("/units")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"id": 1, "name": "Swordsman", "attack": 10},
        {"id": 2, "name": "Archer", "attack": 8},
    ]


# Test get_unit_by_id endpoint
@patch("routes.unit.get_db_connection")
def test_get_unit_by_id(mock_get_db, client):
    mock_db_response(
        mock_get_db, {"id": 1, "name": "Swordsman", "attack": 10}, fetchone=True
    )

    response = client(units_blueprint).get("/units/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Swordsman", "attack": 10}
