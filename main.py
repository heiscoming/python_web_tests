from flask import Flask, jsonify, request
import pymongo
from bson import ObjectId
import os

app = Flask(__name__)
connection = pymongo.Connection("localhost", 27017)
if os.environ.get("TEST"):
    db = connection["test_position"]
else:
    db = connection["position"]


def insert_to_db(data):
    return str(db.position.insert(data))


def get_from_db(data={}, limit=10):
    data = db.position.find(data).limit(limit)
    new_data = []
    for i in data:
        i["_id"] = str(i["_id"])
        new_data.append(i)
    return new_data


def is_correct_coordinates(lat, lon):
    def check(a):
        if len(a) <= 10 and "." in a:  # decrement it
            return True
        else:
            return False
    return check(lat) and check(lon)


def delete_from_db(pos_id=""):
    if pos_id:
        if db.position.find_one({"_id": ObjectId(pos_id)}):
            db.position.remove({"_id": ObjectId(pos_id)})
            return True
        else:
            return False
    if not db.position.drop():
        return True

@app.route("/position", methods=["POST", "GET", "DELETE"])
def position():
    if request.method == "POST":
        lat = request.json.get("lat")
        lon = request.json.get("lon")
        if is_correct_coordinates(lat=lat, lon=lon):
            data = insert_to_db({"lat": lat, "long": lon})
            return jsonify(id=data)
        else:
            return jsonify(message="wrong data")
    if request.method == "GET":
        limit = request.args.get("limit") or 0
        try:
            limit = int(limit)
        except:
            return jsonify(message="limit should be positive integer")
        data = get_from_db(limit=limit)
        return jsonify(positions=data)
    if request.method == "DELETE":
        _id = request.args.get("id")
        if _id:
            if delete_from_db(_id):
                return jsonify(message="position removed")
        else:
            if delete_from_db():
                return jsonify(message="database clear")


@app.route("/")
def main():
    return jsonify(main=True)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, x-xsrf-token')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
    return response

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return jsonify(message='Server shutting down...')

if __name__ == "__main__":
    app.debug = True
    app.run()

