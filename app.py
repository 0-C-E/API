"""
File: app.py
Author: Vianney Veremme
Date: 2024-11-11
Description: This file contains a simple Flask application with two routes.
"""

import datetime

from flask import Flask, jsonify, redirect
from flask_cors import CORS

from config import Config, limiter
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

if app.config["TESTING"]:
    limiter.enabled = False


@app.route("/", methods=["GET"])
def home():
    return redirect("/time")


@app.route("/time", methods=["GET"])
def server_time():
    return jsonify(server_time=datetime.datetime.now().isoformat())


# Register all routes
register_routes(app)


# Add a status field to all JSON responses
@app.after_request
def add_status(response):
    if response.is_json:
        original_data = response.get_json()
        new_response = {
            "success": response.status_code in range(200, 300),
            "data": original_data if original_data != [] else None,
        }
        response.set_data(jsonify(new_response).data)
    return response


@app.after_request
def add_common_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.errorhandler(429)
def ratelimit_error(e):
    return (
        jsonify(
            {
                "error": "Too many requests",
                "message": "Rate limit exceeded. Please try again later.",
                "rate_limit": e.description,
            }
        ),
        429,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
