from flask import Blueprint, jsonify

from db import get_db_connection

worlds_blueprint = Blueprint("worlds", __name__)


@worlds_blueprint.route("", methods=["GET"])
def get_all_worlds():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_worlds")
        worlds = cursor.fetchall()
    db.close()

    return jsonify(worlds)


@worlds_blueprint.route("/<int:world_id>", methods=["GET"])
def get_world_by_id(world_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_world_by_id", (world_id,))
        world = cursor.fetchone()
    db.close()

    return jsonify(world)


@worlds_blueprint.route("/active", methods=["GET"])
def get_active_worlds():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_active_worlds")
        worlds = cursor.fetchall()
    db.close()

    return jsonify(worlds)


@worlds_blueprint.route("/<int:world_id>/players", methods=["GET"])
def get_players_in_world(world_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_players_in_world", (world_id,))
        players = cursor.fetchall()
    db.close()

    return jsonify(players)


@worlds_blueprint.route("/<int:world_id>/islands", methods=["GET"])
def get_islands_in_world(world_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_islands_in_world", (world_id,))
        islands = cursor.fetchall()
    db.close()

    return jsonify(islands)


@worlds_blueprint.route("/<int:world_id>/cities", methods=["GET"])
def get_cities_in_world(world_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_cities_in_world", (world_id,))
        cities = cursor.fetchall()
    db.close()

    return jsonify(cities)
