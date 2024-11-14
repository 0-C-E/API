from unittest.mock import patch

import pytest
from flask import Flask

from routes.battle import battles_blueprint


# Create a Flask app with the blueprint for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(battles_blueprint, url_prefix="/battles")
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

    response = client.get("/battles")
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

    response = client.get("/battles/1")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == mock_battle


# Test get_battle_units endpoint
@patch("routes.battle.get_db_connection")
def test_get_battle_units(mock_get_db, client):
    mock_db_response(
        mock_get_db,
        [
            {"unit_id": 101, "name": "Swordsman", "count": 50, "side": 0},
            {"unit_id": 102, "name": "Archer", "count": 30, "side": 1},
        ],
    )

    response = client.get("/battles/1/units")
    json_data = response.get_json(force=True)

    assert response.status_code == 200
    assert json_data == [
        {"unit_id": 101, "name": "Swordsman", "count": 50, "side": 0},
        {"unit_id": 102, "name": "Archer", "count": 30, "side": 1},
    ]
