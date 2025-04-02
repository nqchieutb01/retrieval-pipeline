from flask import Flask, jsonify, request
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, MilvusClient

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]

from pymilvus import connections
connections.connect( alias="default", host='milvus_standalone', port='19530')
# client = MilvusClient(host="milvus_standalone", port=19530)
# GET request to retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

# GET request to retrieve a specific item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# POST request to add a new item
@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    if not new_item or not 'name' in new_item:
        return jsonify({"error": "Invalid input"}), 400
    
    new_item['id'] = len(data) + 1
    data.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889, debug=False)