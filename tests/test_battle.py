from unittest.mock import patch

from routes.battle import battles_blueprint
from tests.conftest import mock_db_response


# Test get_all_battles endpoint
@patch("routes.battle.get_db_connection")
def test_get_all_battles(mock_get_db, client):
    mock_battles = [
        {
            "battle_id": 1,
            "attacker_id": 1,
            "defender_id": 2,
            "battle_time": None,
            "winner_id": 2,
            "loser_id": 1,
            "loot_wood": 0,
            "loot_stone": 0,
            "loot_silver": 0,
        },
        {
            "battle_id": 2,
            "attacker_id": 1,
            "defender_id": 2,
            "battle_time": None,
            "winner_id": 1,
            "loser_id": 2,
            "loot_wood": 10,
            "loot_stone": 10,
            "loot_silver": 10,
        },
    ]

    mock_db_response(mock_get_db, mock_battles)

    response = client(battles_blueprint).get("/battles")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == mock_battles


# Test get_battle_by_id endpoint
@patch("routes.battle.get_db_connection")
def test_get_battle_by_id(mock_get_db, client):
    mock_battle = {
        "battle_id": 1,
        "attacker_id": 1,
        "defender_id": 2,
        "battle_time": None,
        "winner_id": 2,
        "loser_id": 1,
        "loot_wood": 0,
        "loot_stone": 0,
        "loot_silver": 0,
    }

    mock_db_response(mock_get_db, mock_battle, fetchone=True)

    response = client(battles_blueprint).get("/battles/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == mock_battle


# Test get_battle_units endpoint
@patch("routes.battle.get_db_connection")
def test_get_battle_units(_, client):
    response = client(battles_blueprint).get("/battles/1/units")
    assert response.status_code == 401
