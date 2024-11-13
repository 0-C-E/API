from flask import Blueprint, jsonify, request
from db import get_db_connection

cities_blueprint = Blueprint("cities", __name__)


@cities_blueprint.route("", methods=["GET"])
def get_all_cities():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_cities")
        player = cursor.fetchall()
    db.close()

    return jsonify(player)


@cities_blueprint.route("/<int:city_id>", methods=["GET"])
def get_city_by_id(city_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_city_by_id", (city_id,))
        city = cursor.fetchone()
    db.close()

    return jsonify(city)
