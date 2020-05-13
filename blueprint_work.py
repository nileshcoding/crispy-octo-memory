from flask import Flask
from flask import request
import jwt
import csv
import json
from functions import *
import time
from flask import Blueprint

work = Blueprint('work',__name__)

path_work = r'data/works.csv'

@work.route('/')
def all_work():
    auth_token = request.json["auth_token"]
    data = jwt.decode(auth_token,key = "Caesar")
    li_work = read(path_work)
    li_all_work_by_user = []
    if data["expire"] > time.time():
        for row in li_work:
            if row["user_id"] == data["user_id"]:
                li_all_work_by_user.append([row["work"],row["status"]])
        return json.dumps(li_all_work_by_user)
    else:
        return json.dumps({"message" : "auth_token expired"})

@work.route('/doneworks',methods = ['POST'])
def work_done():
    auth_token = request.json["auth_token"]
    data = jwt.decode(auth_token,key = "Caesar")
    li_work = read(path_work)
    li_work_done_by_user = []
    if data["expire"] > time.time():
        for row in li_work:
            if row["user_id"] == data["user_id"] and row["status"] == "done":
                li_work_done_by_user.append([row["work"],row["status"]])
        return json.dumps(li_work_done_by_user)
    else:
        return json.dumps({"message" : "auth token expired"})

@work.route('/deleteworkdone',methods = ['DELETE'])
def delete_work_done():
    auth_token = request.json["auth_token"]
    data = jwt.decode(auth_token,key="Caesar")
    li_work = read(path_work)
    if data["expire"] > time.time():
        for row in li_work:
            if row["user_id"] == data["user_id"] and row["status"] == "done":
                li_work.remove(row)
        overwrite_file(path_work,li_work)
        return json.dumps({"message" : "all the done works deleted"})
    else: 
        return json.dumps({"message" : "auth token expured"})

@work.route('/addnewwork',methods = ['POST'])
def add_work():
    auth_token = request.json["auth_token"]
    work = request.json["work"]
    data = jwt.decode(auth_token,key = "Caesar")
    if data["expire"] < time.time():
        return json.dumps({"message" : "auth token expired"})
    else:
        li_work = read(path_work)
        id = int(li_work[-1]["id"])+1
        user_id = data["user_id"]
        header = ["id","work","status","user_id"]
        value = {"id" :id,"work" : work, "status" : "not done", "user_id" : user_id}
        append_row(path_work,header,value)
        return json.dumps({"message" : "work added with status not done"})

@work.route('/modifytodonestatus',methods = ['PATCH'])
def modify_status():
    auth_token = request.json["auth_token"]
    data = jwt.decode(auth_token,key = "Caesar")
    if data["expire"] > time.time():
        work = request.json["work"]
        li_work = read(path_work)
        for row in li_work:
            if row["user_id"] == data["user_id"] and row["work"] == work:
                row["status"] = "done"
                overwrite_file(path_work,li_work)
                return json.dumps({"message" : "status changed to done"})
    else:
        return json.dumps({"message" : "auth token expired"})

@work.route('/notdoneworks',methods = ['POST'])
def work_not_done():
    auth_token = request.json["auth_token"]
    data = jwt.decode(auth_token,key = "Caesar")
    li_work = read(path_work)
    li_work_not_done_by_user = []
    if data["expire"] > time.time():
        for row in li_work:
            if row["user_id"] == data["user_id"] and row["status"] == "not done":
                li_work_not_done_by_user.append([row["work"],row["status"]])
        return json.dumps(li_work_not_done_by_user)
    else:
        return json.dumps({"message" : "auth token expired"})