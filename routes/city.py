from flask import Blueprint, jsonify, request
from db import get_db_connection

cities_blueprint = Blueprint("cities", __name__)
