from unittest.mock import patch

import pytest
from flask import Flask

from routes.unit import units_blueprint


# Create a Flask app with the blueprint for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(units_blueprint, url_prefix="/units")
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

    response = client.get("/units")
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

    response = client.get("/units/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Swordsman", "attack": 10}
