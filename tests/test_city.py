from unittest.mock import patch

from routes.city import cities_blueprint
from tests.conftest import mock_db_response


# Test get_all_cities endpoint
@patch("routes.city.get_db_connection")
def test_get_all_cities(mock_get_db, client):
    mock_db_response(
        mock_get_db, [{"id": 1, "name": "CityA"}, {"id": 2, "name": "CityB"}]
    )

    response = client(cities_blueprint).get("/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "CityA"}, {"id": 2, "name": "CityB"}]


# Test get_city_by_id endpoint
@patch("routes.city.get_db_connection")
def test_get_city_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "CityA"}, fetchone=True)

    response = client(cities_blueprint).get("/cities/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "CityA"}


# Test get_city_buildings endpoint
@patch("routes.city.get_db_connection")
def test_get_city_buildings(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"building_id": 1, "name": "Barracks"}, {"building_id": 2, "name": "Academy"}],
    )

    response = client(cities_blueprint).get("/cities/1/buildings")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"building_id": 1, "name": "Barracks"},
        {"building_id": 2, "name": "Academy"},
    ]


# Test get_city_units endpoint
@patch("routes.city.get_db_connection")
def test_get_city_units(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"unit_id": 101, "name": "Infantry"}, {"unit_id": 102, "name": "Cavalry"}],
    )

    response = client(cities_blueprint).get("/cities/1/units")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"unit_id": 101, "name": "Infantry"},
        {"unit_id": 102, "name": "Cavalry"},
    ]
