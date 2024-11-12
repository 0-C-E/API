"""
File: app.py
Author: Vianney Veremme
Date: 2024-11-11
Description: This file contains a simple Flask application with two routes.
"""

import time

from flask import Flask, jsonify, redirect

from routes import register_routes

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return redirect("/time")


@app.route("/time", methods=["GET"])
def server_time():
    return jsonify(server_time=time.strftime("%H:%M:%S %d/%m/%Y"))


# Register all routes
register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
