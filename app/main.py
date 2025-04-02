from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from app.models.bge_m3 import BGEM3Model
from app.database.milvus_client import MilvusClientCustom
from flask import Flask, jsonify, request


# app = FastAPI()
app = Flask(__name__)

model = BGEM3Model()
import time
milvus_client = MilvusClientCustom()

# Pydantic model for request validation
class InsertRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10

@app.route("/insert/", methods=['POST'])
def insert_document():
    try:
        # Parse and validate request data
        data = request.get_json()
        insert_request = InsertRequest(**data)
        
        # Process the request
        embedding = model.encode(insert_request.text)
        print(embedding)
        milvus_client.insert(insert_request.text, embedding)
        return jsonify({"message": "Document inserted successfully"}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@app.route("/search/", methods=['POST'])
def search_documents():
    try:
        # Parse and validate request data
        data = request.get_json()
        search_request = SearchRequest(**data)
        
        # Process the request
        query_embedding = model.encode(search_request.query)
        results = milvus_client.search(query_embedding, search_request.top_k)
        return jsonify({"results": [{"text": hit.entity.text} for hit in results[0]]}), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

import time
if __name__ == '__main__':
    # time.sleep(50)
    app.run(host='0.0.0.0', port=8889, debug=False)