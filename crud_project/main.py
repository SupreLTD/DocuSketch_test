from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from pymongo import MongoClient
from bson import json_util
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from config import settings

app = Flask(__name__)

client = MongoClient(settings.DB_URL)
db: Database = client.test_database
db.items.create_index("key", unique=True)


class Item(BaseModel):
    key: str
    value: str


@app.route('/item', methods=['POST'])
def create_item():
    try:
        item = Item(**request.json)

        try:
            db.items.insert_one(item.dict())
        except DuplicateKeyError as e:
            return jsonify(success=False, message=f'key <{item.key}> already exists'), 409

        return jsonify(success=True, message="Item created."), 201

    except ValidationError as e:
        return jsonify(success=False, message=str(e)), 400


@app.route('/item', methods=['GET', 'PUT'])
def item():
    key = request.args.get('key')

    if request.method == 'GET':
        item = db.items.find_one({"key": key})
        if item:
            return json_util.dumps(item), 200
        else:
            return jsonify(success=False, message="Item not found."), 404

    elif request.method == 'PUT':
        new_value = request.json.get('value')
        result = db.items.update_one({"key": key}, {"$set": {"value": new_value}})
        if result.matched_count:
            return jsonify(success=True, message="Item updated."), 200
        else:
            return jsonify(success=False, message="Item not found."), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
