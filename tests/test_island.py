from unittest.mock import patch

import pytest
from flask import Flask

from routes.island import islands_blueprint


# Create a Flask app with the blueprint for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(islands_blueprint, url_prefix="/islands")
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


# Test get_all_islands endpoint
@patch("routes.island.get_db_connection")
def test_get_all_islands(mock_get_db, client):
    mock_db_response(
        mock_get_db, [{"id": 1, "name": "Island1"}, {"id": 2, "name": "Island2"}]
    )

    response = client.get("/islands")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "Island1"}, {"id": 2, "name": "Island2"}]


# Test get_island_by_id endpoint
@patch("routes.island.get_db_connection")
def test_get_island_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Island1"}, fetchone=True)

    response = client.get("/islands/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Island1"}


# Test get_island_cities endpoint
@patch("routes.island.get_db_connection")
def test_get_island_cities(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"city_id": 101, "name": "CityA"}, {"city_id": 102, "name": "CityB"}],
    )

    response = client.get("/islands/1/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"city_id": 101, "name": "CityA"},
        {"city_id": 102, "name": "CityB"},
    ]
