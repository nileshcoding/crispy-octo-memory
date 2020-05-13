from flask import Flask
from flask import request
import jwt
import csv
import json
from functions import *
import time
from blueprint_work import work

app = Flask(__name__)
app.register_blueprint(work, url_prefix = '/work')
path_user = r'data/users.csv'

@app.route('/')
def home_todo():
    return json.dumps({"message" : "to do list homepage"})

@app.route('/login',methods = ['POST'])
def login_todo():
    username = request.json["username"]
    password = request.json["password"]
    li_user = read(path_user)
    for row in li_user:
        if row["username"] == username and row["password"] == password:
            id = row["id"]
            payload = {"user_id" : id, "name" : row["name"],"message" : "logged in", "expire" : time.time()+3600}
            encoded_jwt = jwt.encode(payload,key="Caesar")
            return json.dumps({"auth_token" : encoded_jwt.decode(),"message" : "logged in"})
    return json.dumps({"message" : "username or password incorrect"})

@app.route('/user/register',methods = ['POST'])
def register_user():
    li_user = read(path_user)
    name = request.json["name"]
    username = request.json["username"]
    password = request.json["password"]
    id = int(li_user[-1]["id"])+1
    header = ["id","name","username","password"]
    value = {"id" : id, "name" : name, "username" : username,"password" : password}
    append_row(path_user,header,value)
    return json.dumps({"message" : "user registered"})