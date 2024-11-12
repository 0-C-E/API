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
