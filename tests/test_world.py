from unittest.mock import patch

from routes.world import worlds_blueprint
from tests.conftest import mock_db_response


# Test get_all_worlds endpoint with enhanced attribute validation
@patch("routes.world.get_db_connection")
def test_get_all_worlds(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {
                "world_id": 1,
                "world_name": "World1",
                "world_description": "First test world",
                "seed": 1234,
                "action_speed": 2,
                "unit_speed": 2,
                "trade_speed": 1,
                "night_bonus": 1,
                "beginner_protection": 7,
                "morale": True,
                "world_status": 1,
                "created_at": "2024-01-01T00:00:00",
            }
        ],
    )

    response = client(worlds_blueprint).get("/worlds")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data[0]["world_id"] == 1
    assert json_data[0]["world_name"] == "World1"
    assert json_data[0]["morale"] is True
    assert json_data[0]["world_status"] == 1
    assert json_data[0]["created_at"] == "2024-01-01T00:00:00"


# Test get_world_by_id endpoint with enhanced response data validation
@patch("routes.world.get_db_connection")
def test_get_world_by_id(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        {
            "world_id": 1,
            "world_name": "World1",
            "world_description": "Test world with specific ID",
            "seed": 4321,
            "action_speed": 2,
            "unit_speed": 1,
            "trade_speed": 2,
            "night_bonus": 0,
            "beginner_protection": 5,
            "morale": False,
            "world_status": 1,
            "created_at": "2024-01-01T12:00:00",
        },
        fetchone=True,
    )

    response = client(worlds_blueprint).get("/worlds/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data["world_id"] == 1
    assert json_data["world_name"] == "World1"
    assert json_data["morale"] is False
    assert json_data["world_status"] == 1
    assert json_data["created_at"] == "2024-01-01T12:00:00"


# Test get_active_worlds endpoint, ensuring all returned worlds are active
@patch("routes.world.get_db_connection")
def test_get_active_worlds(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {
                "world_id": 1,
                "world_name": "ActiveWorld1",
                "world_description": "Active world",
                "created_at": "2024-01-02T00:00:00",
            },
            {
                "world_id": 2,
                "world_name": "ActiveWorld2",
                "world_description": "Another active world",
                "created_at": "2024-01-03T00:00:00",
            },
        ],
    )

    response = client(worlds_blueprint).get("/worlds/active")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    for world in json_data:
        assert "world_id" in world
        assert "world_name" in world
        assert "created_at" in world


# Test get_players_in_world endpoint for players in a specific world
@patch("routes.world.get_db_connection")
def test_get_players_in_world(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {
                "player_id": 101,
                "player_name": "PlayerA",
                "email": "playera@example.com",
            },
            {
                "player_id": 102,
                "player_name": "PlayerB",
                "email": "playerb@example.com",
            },
        ],
    )

    response = client(worlds_blueprint).get("/worlds/1/players")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"player_id": 101, "player_name": "PlayerA", "email": "playera@example.com"},
        {"player_id": 102, "player_name": "PlayerB", "email": "playerb@example.com"},
    ]


# Test get_islands_in_world endpoint with empty response (no islands in world)
@patch("routes.world.get_db_connection")
def test_get_islands_in_world_empty(mock_get_db, client):
    mock_db_response(mock_get_db, [])

    response = client(worlds_blueprint).get("/worlds/2/islands")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == []


# Test get_islands_in_world endpoint with multiple islands in world
@patch("routes.world.get_db_connection")
def test_get_islands_in_world(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {"island_id": 201, "x": 100, "y": 200},
            {"island_id": 202, "x": 150, "y": 250},
        ],
    )

    response = client(worlds_blueprint).get("/worlds/1/islands")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"island_id": 201, "x": 100, "y": 200},
        {"island_id": 202, "x": 150, "y": 250},
    ]


# Test get_cities_in_world endpoint for world with multiple cities
@patch("routes.world.get_db_connection")
def test_get_cities_in_world(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {"city_id": 301, "city_name": "CityA", "owner_id": 101, "island_id": 201},
            {"city_id": 302, "city_name": "CityB", "owner_id": 102, "island_id": 202},
        ],
    )

    response = client(worlds_blueprint).get("/worlds/1/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"city_id": 301, "city_name": "CityA", "owner_id": 101, "island_id": 201},
        {"city_id": 302, "city_name": "CityB", "owner_id": 102, "island_id": 202},
    ]


# Additional test case: get_cities_in_world endpoint with a world that has no cities
@patch("routes.world.get_db_connection")
def test_get_cities_in_world_empty(mock_get_db, client):
    mock_db_response(mock_get_db, [])

    response = client(worlds_blueprint).get("/worlds/3/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == []
