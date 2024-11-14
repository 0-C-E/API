from flask import Blueprint, jsonify, request

from db import get_db_connection

buildings_blueprint = Blueprint("buildings", __name__)


@buildings_blueprint.route("", methods=["GET"])
def get_all_buildings():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_buildings")
        buildings = cursor.fetchall()
    db.close()

    return jsonify(buildings)


@buildings_blueprint.route("/<int:building_id>", methods=["GET"])
def get_building_by_id(building_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_building_by_id", (building_id,))
        building = cursor.fetchone()
    db.close()

    return jsonify(building)


@buildings_blueprint.route("/<int:building_id>/prerequisites", methods=["GET"])
def get_building_prerequisites(building_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_building_prerequisites", (building_id,))
        prerequisites = cursor.fetchall()
    db.close()

    return jsonify(prerequisites)
