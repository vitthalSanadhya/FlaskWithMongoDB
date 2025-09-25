from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

# MongoDB connection
MONGO_URI = "mongodb+srv://vitthalsanadhya_db_user:Vitthal%402001@flaskappcluster.fjifvmh.mongodb.net/?retryWrites=true&w=majority&appName=FlaskAppCluster"
client = MongoClient(MONGO_URI)
db = client.mymongodb
todos = db.todo

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

@app.route("/list")
def lists():
    try:
        todos_l = todos.find()
        a1 = "active"
        return render_template('index.html', a1=a1, todos=todos_l, t=title, h=heading)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
@app.route("/uncompleted")
def tasks():
    try:
        todos_l = todos.find({"done": "no"})
        a2 = "active"
        return render_template('index.html', a2=a2, todos=todos_l, t=title, h=heading)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/completed")
def completed():
    try:
        todos_l = todos.find({"done": "yes"})
        a3 = "active"
        return render_template('index.html', a3=a3, todos=todos_l, t=title, h=heading)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/done")
def done():
    try:
        id = request.values.get("_id")
        task = todos.find_one({"_id": ObjectId(id)})
        if task:
            new_status = "no" if task["done"] == "yes" else "yes"
            todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": new_status}})
        return redirect(redirect_url())
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/action", methods=['POST'])
def action():
    try:
        name = request.values.get("name") or ""
        desc = request.values.get("desc") or ""
        date = request.values.get("date") or ""
        pr = request.values.get("pr") or ""
        todos.insert_one({"name": name, "desc": desc, "date": date, "pr": pr, "done": "no"})
        return redirect("/list")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/remove")
def remove():
    try:
        key = request.values.get("_id")
        todos.delete_one({"_id": ObjectId(key)})
        return redirect("/")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/update")
def update():
    try:
        id = request.values.get("_id")
        task = todos.find({"_id": ObjectId(id)})
        return render_template('update.html', tasks=task, h=heading, t=title)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/action3", methods=['POST'])
def action3():
    try:
        name = request.values.get("name") or ""
        desc = request.values.get("desc") or ""
        date = request.values.get("date") or ""
        pr = request.values.get("pr") or ""
        id = request.values.get("_id")
        todos.update_one({"_id": ObjectId(id)}, {'$set': {"name": name, "desc": desc, "date": date, "pr": pr}})
        return redirect("/")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/search", methods=['GET'])
def search():
    try:
        key = request.values.get("key")
        refer = request.values.get("refer")
        if key == "_id":
            todos_l = todos.find({refer: ObjectId(key)})
        else:
            todos_l = todos.find({refer: key})
        return render_template('searchlist.html', todos=todos_l, t=title, h=heading)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # debug=True for now to see full errors
