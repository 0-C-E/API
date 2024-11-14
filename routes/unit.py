from flask import Blueprint, jsonify

from db import get_db_connection

units_blueprint = Blueprint("units", __name__)


@units_blueprint.route("", methods=["GET"])
def get_all_units():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_units")
        units = cursor.fetchall()
    db.close()

    return jsonify(units)


@units_blueprint.route("/<int:unit_id>", methods=["GET"])
def get_unit_by_id(unit_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_unit_by_id", (unit_id,))
        unit = cursor.fetchone()
    db.close()

    return jsonify(unit)
