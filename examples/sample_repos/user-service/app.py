from flask import Flask, request
app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    password = "supersecret"  # hardcoded for testing detection
    return {"token": "fake-jwt-token"}
