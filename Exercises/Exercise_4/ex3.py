#!/usr/bin/env python3
import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

## This method returns a list of messages in a json format such as 
## [
##  { "name": <name>, "message": <message> },
##  { "name": <name>, "message": <message> },
##  ...
## ]
## If this is a POST request and there is a parameter "name" given, then only
## messages of the given name should be returned.
## If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages",methods=["GET","POST"])
def messages():
    with db.cursor() as cursor:
        # TODO: Return 500 if POST parameter is invalid, check if name is valid, regex??? Don't need to to get the token, because of the test probably
        sql = "SELECT name, message FROM messages"
        result = None
        if request.method == "POST":
            name = request.form["name"]
            sql += " WHERE name = %s"
            cursor.execute(sql, (name))
            result = cursor.fetchall()
        else:
            cursor.execute(sql)
            result = cursor.fetchall()

        out_json = []
        for r in result:
            out_json.append({ "name": r[0], "message": r[1] }) 
        return jsonify(out_json), 200


## This method returns the list of users in a json format such as
## { "users": [ <user1>, <user2>, ... ] }
## This methods should limit the number of users if a GET URL parameter is given
## named limit. For example, /users?limit=4 should only return the first four
## users.
## If the paramer given is invalid, then the response code must be 500.
@app.route("/users",methods=["GET"])
def contact():
    with db.cursor() as cursor:
        sql = "SELECT name FROM users"
        cursor.execute(sql)
        
        user_list = []
        limit = request.args.get("limit")
        if limit != None:
            if not limit.isdigit():
                return "Fitte", 500  # Code doesn't work when returning 500.....
            value = int(limit)

            # Can use LIMIT as I can't find a function for cursor to see how many records are in the db...
            result = cursor.fetchall()
            if len(result) < value:
                value = len(result)
            user_list = [user_list.append(result[i][0]) for i in range(value)]
        else:
            users = cursor.fetchall()
            for u in users:
                user_list.append(u[0])
        json = {"users": user_list}
        return jsonify(json), 200


if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    db = pymysql.connect("localhost",
                username,
                password,
                database)
    with db.cursor() as cursor:
        populate.populate_db(seed,cursor)             
        db.commit()
    print("[+] database populated")

    app.run(host='0.0.0.0',port=80)




"""
CURLS FOR TASK 3

curl -d '{"name": "malden"}' -H "Content-Type: application/json" -X POST http://0.0.0.0:80/messages

curl -X POST -F 'name=malden' http://0.0.0.0:80/messages

curl -X POST http://0.0.0.0:80/messages and curl -X POST -F '' http://0.0.0.0:80/messages is not allowed!

curl http://0.0.0.0:80/messages

curl http://0.0.0.0:80/users

http://0.0.0.0:80/users?limit=5
"""