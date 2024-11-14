from unittest.mock import patch

from routes.player import players_blueprint
from tests.conftest import mock_db_response

mock_player_data = [
    {
        "player_id": 1,
        "player_name": "Player1",
        "email": "player1@example.com",
        "gold": 100,
        "created_at": "2023-01-01T12:00:00Z",
        "last_login": "2023-01-02T12:00:00Z",
    }
]


# Test get_all_players endpoint
@patch("routes.player.get_db_connection")
def test_get_all_players(mock_get_db, client):
    mock_db_response(mock_get_db, mock_player_data)

    response = client(players_blueprint).get("/players")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == mock_player_data


# Test get_player_by_id endpoint
@patch("routes.player.get_db_connection")
def test_get_player_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, mock_player_data[0], fetchone=True)

    response = client(players_blueprint).get("/players/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == mock_player_data[0]


# Test get_player_by_name endpoint
@patch("routes.player.get_db_connection")
def test_get_player_by_name(mock_get_db, client):
    mock_db_response(mock_get_db, mock_player_data[0], fetchone=True)

    response = client(players_blueprint).get("/players/Player1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == mock_player_data[0]


# Test get_player_worlds endpoint
@patch("routes.player.get_db_connection")
def test_get_player_worlds(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {
                "world_id": 1,
                "world_name": "World1",
                "world_description": "The first world",
                "created_at": "2023-01-01T12:00:00Z",
            }
        ],
    )

    response = client(players_blueprint).get("/players/1/worlds")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {
            "world_id": 1,
            "world_name": "World1",
            "world_description": "The first world",
            "created_at": "2023-01-01T12:00:00Z",
        }
    ]


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
    mock_db_response(
        mock_get_db, [{"city_id": 101, "city_name": "CityA", "island_id": 10}]
    )

    response = client(players_blueprint).get("/players/1/cities?world_id=1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"city_id": 101, "city_name": "CityA", "island_id": 10}]


# Test get_player_battles endpoint
@patch("routes.player.get_db_connection")
def test_get_player_battles(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {
                "battle_id": 1,
                "attacker_id": 1,
                "defender_id": 2,
                "battle_time": "2023-01-01T12:00:00Z",
                "winner_id": 1,
                "loser_id": 2,
                "loot_wood": 50,
                "loot_stone": 30,
                "loot_silver": 20,
            }
        ],
    )

    response = client(players_blueprint).get("/players/1/battles")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {
            "battle_id": 1,
            "attacker_id": 1,
            "defender_id": 2,
            "battle_time": "2023-01-01T12:00:00Z",
            "winner_id": 1,
            "loser_id": 2,
            "loot_wood": 50,
            "loot_stone": 30,
            "loot_silver": 20,
        }
    ]
