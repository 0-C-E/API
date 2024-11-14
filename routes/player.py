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


@players_blueprint.route("/<int:player_id>/worlds", methods=["GET"])
def get_player_worlds(player_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_player_worlds", (player_id,))
        worlds = cursor.fetchall()
    db.close()

    return jsonify(worlds)


@players_blueprint.route("/<int:player_id>/cities", methods=["GET"])
def get_player_cities(player_id):
    world_id = request.args.get("world_id")

    if not world_id:
        return jsonify({"error": "Missing 'world_id' parameter"}), 400

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc(
            "get_player_cities",
            (
                world_id,
                player_id,
            ),
        )
        cities = cursor.fetchall()
    db.close()

    return jsonify(cities)


@players_blueprint.route("/<int:player_id>/battles", methods=["GET"])
def get_player_battles(player_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_player_battles", (player_id,))
        battles = cursor.fetchall()
    db.close()

    return jsonify(battles)
