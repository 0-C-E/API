from flask import Blueprint, jsonify, request
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
