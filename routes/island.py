from flask import Blueprint, jsonify, request
from db import get_db_connection

islands_blueprint = Blueprint("islands", __name__)
