import os
from re import match

from argon2 import PasswordHasher, exceptions
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from pymysql import MySQLError

from db import get_db_connection

load_dotenv()

authentication_blueprint = Blueprint("authentication", __name__)
ph = PasswordHasher()


def hash_password_with_salt_and_pepper(password: str) -> str:
    salt = os.urandom(16)
    pepper = os.getenv("PEPPER").encode("utf-8")
    seasoned_password = password.encode("utf-8") + salt + pepper
    return ph.hash(seasoned_password), salt


def validate_password(password):
    """
    Validates a password based on the following criteria:
    - At least 12 characters long.
    - Contains at least one uppercase letter (A-Z).
    - Contains at least one lowercase letter (a-z).
    - Contains at least one digit (0-9).
    - Contains at least one special character (any non-alphanumeric character).
    """
    return bool(
        match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$", password)
    )


@authentication_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify(message="Username, email, and password are required"), 400

    if not validate_password(password):
        return jsonify(message="Password does not meet security requirements"), 400

    hashed_password, salt = hash_password_with_salt_and_pepper(password)

    db = get_db_connection()
    with db.cursor() as cursor:
        try:
            cursor.callproc("register_player", (name, email, hashed_password, salt))
            db.commit()
        except MySQLError as e:
            if e.args[0] == 1644:
                return jsonify(message="Email already in use"), 400
            else:
                return jsonify(message="An error occurred during registration"), 500

    db.close()
    return jsonify(message="User created successfully"), 201


@authentication_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(message="Email and password are required"), 400

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT hashed_password, salt FROM player WHERE email = %s", (email,)
        )
        player = cursor.fetchone()

        if not player:
            return jsonify(message="Invalid credentials"), 401

        stored_password = player["hashed_password"]
        salt = player["salt"]
        pepper = os.getenv("PEPPER").encode("utf-8")
        seasoned_password = password.encode("utf-8") + salt + pepper

        try:
            ph.verify(stored_password, seasoned_password)
            return jsonify(message="Login successful"), 200
        except exceptions.VerifyMismatchError:
            return jsonify(message="Invalid credentials"), 401
