from flask import Flask, jsonify, redirect
import time

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return redirect("/time")


@app.route("/time", methods=["GET"])
def server_time():
    return jsonify(server_time=time.strftime("%H:%M:%S %d/%m/%Y"))
