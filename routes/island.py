from flask import Blueprint, jsonify

from db import get_db_connection

islands_blueprint = Blueprint("islands", __name__)


@islands_blueprint.route("", methods=["GET"])
def get_all_islands():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_islands")
        islands = cursor.fetchall()
    db.close()

    return jsonify(islands)


@islands_blueprint.route("/<int:island_id>", methods=["GET"])
def get_island_by_id(island_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_island_by_id", (island_id,))
        island = cursor.fetchone()
    db.close()

    return jsonify(island)


@islands_blueprint.route("/<int:island_id>/cities", methods=["GET"])
def get_island_cities(island_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_island_cities", (island_id,))
        cities = cursor.fetchall()
    db.close()

    return jsonify(cities)
