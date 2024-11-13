from flask import Blueprint, jsonify, request
from db import get_db_connection

players_blueprint = Blueprint("players", __name__)


@players_blueprint.route("", methods=["GET"])
def get_all_players():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_players")
        players = cursor.fetchall()
    db.close()

    return jsonify(players)


@players_blueprint.route("/<int:player_id>", methods=["GET"])
def get_player_by_id(player_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_player_by_id", (player_id,))
        player = cursor.fetchone()
    db.close()

    return jsonify(player)


@players_blueprint.route("/<string:player_name>", methods=["GET"])
def get_player_by_name(player_name):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_player_by_name", (player_name,))
        player = cursor.fetchone()
    db.close()

    return jsonify(player)
