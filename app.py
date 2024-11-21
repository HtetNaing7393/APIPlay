import requests
import semver
import re
import json
from flask import Flask, redirect, request, render_template, jsonify
from utilities.functions import execute, display_success
from fetch_google import get_api_data



#################### Web Server and Display ####################

# Web-Page running
app = Flask(__name__)

# @app.route("/get_data", methods=["POST"])
def get_data():
    result = "This is test data"
    return jsonify(result=result)


@app.route("/")
def home():
    # data = execute("https://api.apis.guru/v2/list.json")
    # return render_template("home.html", info=info, header=header, body=body)
    return render_template("home.html")

@app.route("/button-click", methods = ["POST"])
def button_click():
    result = execute("https://api.apis.guru/v2/list.json")
    print(result)
    return result

if __name__ == "__main__":
    app.run(debug=True)
