from flask import Blueprint, jsonify, request
from db import get_db_connection

battles_blueprint = Blueprint("battles", __name__)
