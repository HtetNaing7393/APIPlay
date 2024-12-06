import requests
import semver
import re
import json
from flask import Flask, redirect, request, render_template, jsonify
from utilities.functions import execute




#################### Web Server and Display ####################

# Web-Page running
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/button-click", methods = ["POST"])
def button_click():
    result = execute("https://api.apis.guru/v2/list.json")
    output = json.dumps(result)
    return output

if __name__ == "__main__":
    app.run(debug=True)
