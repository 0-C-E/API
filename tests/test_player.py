from unittest.mock import patch

from routes.player import players_blueprint
from tests.conftest import mock_db_response


@patch("routes.player.get_db_connection")
def test_get_all_players(mock_get_db, client):
    mock_db_response(mock_get_db, [{"id": 1, "name": "Player1"}])

    response = client(players_blueprint).get("/players")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "Player1"}]


# Test get_player_by_id endpoint
@patch("routes.player.get_db_connection")
def test_get_player_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Player1"}, fetchone=True)

    response = client(players_blueprint).get("/players/1")
    json_data = response.get_json(force=True)
    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Player1"}


# Test get_player_by_name endpoint
@patch("routes.player.get_db_connection")
def test_get_player_by_name(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "Player1"}, fetchone=True)

    response = client(players_blueprint).get("/players/Player1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "Player1"}


# Test get_player_cities endpoint with missing 'world_id' parameter
@patch("routes.player.get_db_connection")
def test_get_player_cities_missing_world_param(mock_get_db, client):
    response = client(players_blueprint).get("/players/1/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 400
    assert json_data == {"error": "Missing 'world_id' parameter"}


# Test get_player_cities endpoint with valid 'world_id' parameter
@patch("routes.player.get_db_connection")
def test_get_player_cities_with_world_param(mock_get_db, client):
    mock_db_response(mock_get_db, [{"city_id": 101, "name": "CityA"}])

    response = client(players_blueprint).get("/players/1/cities?world_id=1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"city_id": 101, "name": "CityA"}]
