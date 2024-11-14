from unittest.mock import patch

from routes.world import worlds_blueprint
from tests.conftest import mock_db_response


# Test get_all_worlds endpoint
@patch("routes.world.get_db_connection")
def test_get_all_worlds(mock_get_db, client):
    mock_db_response(
        mock_get_db, [{"id": 1, "name": "World1"}, {"id": 2, "name": "World2"}]
    )

    response = client(worlds_blueprint).get("/worlds")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "World1"}, {"id": 2, "name": "World2"}]


# Test get_world_by_id endpoint
@patch("routes.world.get_db_connection")
def test_get_world_by_id(mock_get_db, client):
    mock_db_response(mock_get_db, {"id": 1, "name": "World1"}, fetchone=True)

    response = client(worlds_blueprint).get("/worlds/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == {"id": 1, "name": "World1"}


# Test get_active_worlds endpoint
@patch("routes.world.get_db_connection")
def test_get_active_worlds(mock_get_db, client):
    mock_db_response(mock_get_db, [{"id": 1, "name": "World1"}])

    response = client(worlds_blueprint).get("/worlds/active")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [{"id": 1, "name": "World1"}]


# Test get_players_in_world endpoint
@patch("routes.world.get_db_connection")
def test_get_players_in_world(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"player_id": 101, "name": "PlayerA"}, {"player_id": 102, "name": "PlayerB"}],
    )

    response = client(worlds_blueprint).get("/worlds/1/players")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"player_id": 101, "name": "PlayerA"},
        {"player_id": 102, "name": "PlayerB"},
    ]


# Test get_islands_in_world endpoint
@patch("routes.world.get_db_connection")
def test_get_islands_in_world(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"island_id": 201, "name": "IslandX"}, {"island_id": 202, "name": "IslandY"}],
    )

    response = client(worlds_blueprint).get("/worlds/1/islands")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"island_id": 201, "name": "IslandX"},
        {"island_id": 202, "name": "IslandY"},
    ]


# Test get_cities_in_world endpoint
@patch("routes.world.get_db_connection")
def test_get_cities_in_world(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [{"city_id": 301, "name": "CityA"}, {"city_id": 302, "name": "CityB"}],
    )

    response = client(worlds_blueprint).get("/worlds/1/cities")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"city_id": 301, "name": "CityA"},
        {"city_id": 302, "name": "CityB"},
    ]
