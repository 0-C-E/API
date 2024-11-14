from unittest.mock import patch

import pytest
from flask import Flask

from routes.building import buildings_blueprint


# Create a Flask app with the blueprint for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(buildings_blueprint, url_prefix="/buildings")
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


# Test get_all_buildings endpoint
@patch("routes.building.get_db_connection")
def test_get_all_buildings(mock_get_db, client):
    mock_db_response(
        mock_get_db, [{"id": 1, "name": "Barracks"}, {"id": 2, "name": "Academy"}]
    )

    response = client.get("/buildings")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "Barracks"}, {"id": 2, "name": "Academy"}]


# Test get_building_by_id endpoint
@patch("routes.building.get_db_connection")
def test_get_building_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Barracks"}, fetchone=True)

    response = client.get("/buildings/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Barracks"}


# Test get_building_prerequisites endpoint
@patch("routes.building.get_db_connection")
def test_get_building_prerequisites(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {"required_building_id": 2, "required_level": 3},
            {"required_building_id": 3, "required_level": 2},
        ],
    )

    response = client.get("/buildings/1/prerequisites")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"required_building_id": 2, "required_level": 3},
        {"required_building_id": 3, "required_level": 2},
    ]
