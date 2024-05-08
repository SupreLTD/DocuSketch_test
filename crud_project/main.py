from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://root:example@mongo:27017/")
db = client.test_database


class Item(BaseModel):
    key: str
    value: str


@app.route('/item', methods=['POST'])
def create_item():
    try:
        item = Item(**request.json)
        result = db.items.insert_one(item.dict())
        return jsonify(str(result.inserted_id)), 201
    except ValidationError as e:
        return jsonify(error=str(e)), 400


@app.route('/item/<id>', methods=['GET', 'PUT'])
def get_update_item(id_):
    if request.method == 'GET':
        item = db.items.find_one({"_id": ObjectId(id_)})
        if item:
            return jsonify(item), 200
        else:
            return jsonify(error="Item not found"), 404
    elif request.method == 'PUT':
        try:
            item = Item(**request.json)
            result = db.items.update_one({"_id": ObjectId(id_)}, {"$set": item.dict()})
            if result.modified_count:
                return jsonify(success=True), 200
            else:
                return jsonify(error="No item updated"), 404
        except ValidationError as e:
            return jsonify(error=str(e)), 400


if __name__ == '__main__':
    app.run()
