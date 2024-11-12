from flask import Blueprint, jsonify, request
from db import get_db_connection

buildings_blueprint = Blueprint("buildings", __name__)
