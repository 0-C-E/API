from flask import Blueprint, jsonify

from db import get_db_connection

battles_blueprint = Blueprint("battles", __name__)


@battles_blueprint.route("", methods=["GET"])
def get_all_battles():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_all_battles")
        battles = cursor.fetchall()
    db.close()

    return jsonify(battles)


@battles_blueprint.route("/<int:battle_id>", methods=["GET"])
def get_battle_by_id(battle_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_battle_by_id", (battle_id,))
        battle = cursor.fetchone()
    db.close()

    return jsonify(battle)


@battles_blueprint.route("/<int:battle_id>/units", methods=["GET"])
def get_battle_units(battle_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.callproc("get_battle_units", (battle_id,))
        units = cursor.fetchall()
    db.close()

    return jsonify(units)
