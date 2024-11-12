from flask import Blueprint, jsonify, request
from db import get_db_connection

worlds_blueprint = Blueprint("worlds", __name__)
