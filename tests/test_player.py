from unittest.mock import MagicMock, patch

import pytest
from flask import Flask

from routes.player import players_blueprint


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(players_blueprint, url_prefix="/players")
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def mock_db_response(mock_get_db, data=None, fetchone=False):
    mock_connection = MagicMock()
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
    if fetchone:
        mock_cursor.fetchone.return_value = data
    else:
        mock_cursor.fetchall.return_value = data
    mock_get_db.return_value = mock_connection


@patch("routes.player.get_db_connection")
def test_get_all_players(mock_get_db, client):
    mock_db_response(mock_get_db, [{"id": 1, "name": "Player1"}])

    response = client.get("/players")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "Player1"}]


# Test get_player_by_id endpoint
@patch("routes.player.get_db_connection")
def test_get_player_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Player1"}, fetchone=True)

    response = client.get("/players/1")
    json_data = response.get_json(force=True)
    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Player1"}


# Test get_player_by_name endpoint
@patch("routes.player.get_db_connection")
def test_get_player_by_name(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Player1"}, fetchone=True)

    response = client.get("/players/Player1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Player1"}


# Test get_player_cities endpoint with missing 'world_id' parameter
@patch("routes.player.get_db_connection")
def test_get_player_cities_missing_world_param(mock_get_db, client):
    response = client.get("/players/1/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 400
    assert json_data == {"error": "Missing 'world_id' parameter"}


# Test get_player_cities endpoint with valid 'world_id' parameter
@patch("routes.player.get_db_connection")
def test_get_player_cities_with_world_param(mock_get_db, client):
    mock_db_response(mock_get_db, [{"city_id": 101, "name": "CityA"}])

    response = client.get("/players/1/cities?world_id=1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"city_id": 101, "name": "CityA"}]
