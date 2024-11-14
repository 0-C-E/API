from flask import Blueprint, jsonify

from db import get_db_connection

cities_blueprint = Blueprint("cities", __name__)


@cities_blueprint.route("", methods=["GET"])
def get_all_cities():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_cities")
        cities = cursor.fetchall()
    db.close()

    return jsonify(cities)


@cities_blueprint.route("/<int:city_id>", methods=["GET"])
def get_city_by_id(city_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_city_by_id", (city_id,))
        city = cursor.fetchone()
    db.close()

    return jsonify(city)


@cities_blueprint.route("/<int:city_id>/buildings", methods=["GET"])
def get_city_buildings(city_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_city_buildings", (city_id,))
        buildings = cursor.fetchall()
    db.close()

    return jsonify(buildings)


@cities_blueprint.route("/<int:city_id>/units", methods=["GET"])
def get_city_units(city_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_city_units", (city_id,))
        units = cursor.fetchall()
    db.close()

    return jsonify(units)
