from flask import Flask, jsonify, request
from flask_restful import APi, Resource 
from pymongo import MongoClient 
import bcrypt 
import requests
import subprocess 
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db["Users"]

def UserExists(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExists(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"   
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode("utf8"),bcrypt.gensalt())
        # Insert username in db
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 4
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for this API"
        }
        return jsonify(retJson)