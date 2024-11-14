from unittest.mock import patch

import pytest
from flask import Flask

from routes.city import cities_blueprint


# Create a Flask app with the blueprint for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(cities_blueprint, url_prefix="/cities")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# Utility function to mock database responses
def mock_db_response(mock_get_db, data, fetchone=False):
    mock_cursor = mock_get_db.return_value.cursor.return_value.__enter__.return_value
    if fetchone:
        mock_cursor.fetchone.return_value = data
    else:
        mock_cursor.fetchall.return_value = data


# Test get_all_cities endpoint
@patch("routes.city.get_db_connection")
def test_get_all_cities(mock_get_db, client):
    mock_db_response(
        mock_get_db, [{"id": 1, "name": "CityA"}, {"id": 2, "name": "CityB"}]
    )

    response = client.get("/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "CityA"}, {"id": 2, "name": "CityB"}]


# Test get_city_by_id endpoint
@patch("routes.city.get_db_connection")
def test_get_city_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "CityA"}, fetchone=True)

    response = client.get("/cities/1")
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

    response = client.get("/cities/1/buildings")
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

    response = client.get("/cities/1/units")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"unit_id": 101, "name": "Infantry"},
        {"unit_id": 102, "name": "Cavalry"},
    ]
