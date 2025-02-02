from flask import Flask, jsonify
from flask_cors import CORS
import openai
from flask_caching import Cache
import os
from dotenv import load_dotenv

# Set your OpenAI API key
app = Flask(__name__)
CORS(app)

# Configure cache
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',  # Use 'redis' for production
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
})

load_dotenv()  # Load .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#FOR THIS LEVEL DO NOT INCLUDE EDGES
graph_data_lvl_1 = {
    "nodes": [1, 2, 3, 4, 5, 6],
    "node_names": [
        "Category A",
        "Category B",
        "Category C",
        "Category D",
        "Category E",
        "Category F"
    ],
    "severity": [1, 2, 3, 4, 5, 1],
    "edges": [
        
    ]
}
#FOR THIS LEVEL MAKE THE FIRST NODE THE TOPIC NODE FROM LEVEL 1 AND THE REST THE CATEGORY NODES, ALL THE EDGES SHOULD INCLUDE 1.
graph_data_lvl_2 = {
    "nodes": [1, 2, 3, 4, 5, 6],
    "node_names": [
        "Category A",
        "Category B",
        "Category C",
        "Category D",
        "Category E",
        "Category F"
    ],
    "severity": [1, 2, 3, 4, 5, 1],
    "edges": [ 
        [1, 2],
        [1, 3],
        [1, 3],
        [1, 5],
        [1, 6]
    ],
    "node_name": [
        "Quotes"
    ]
}

graph_data_lvl_3 = {
    "nodes": [1, 2, 3, 4, 5, 6],
    "node_names": [
        "Category A",
        "Category B",
        "Category C",
        "Category D",
        "Category E",
        "Category F"
    ],
    "severity": [1, 2, 3, 4, 5, 1],
    "edges": [
        [1, 2],
        [4, 3],
        [1, 3],
        [4, 5],
        [1, 6]
    ],
    "node_name": [
        "Name of sourse"
    ],
    "link" : ["..."]
}

graph_title_data = {
    "header": "Youtube Video: Trump Inauguration"
}

@app.route('/node_lvl_1', methods=['GET'])
@cache.cached(timeout=300)
def get_data_lvl_1():
    return jsonify(graph_data_lvl_1)

@app.route('/node_lvl_2', methods=['GET'])
@cache.cached(timeout=300)
def get_data_lvl_2():
    return jsonify(graph_data_lvl_2)

@app.route('/node_lvl_3', methods=['GET'])
@cache.cached(timeout=300)
def get_data_lvl_3():
    return jsonify(graph_data_lvl_3)

@app.route('/lvl_2_title')
@cache.cached(timeout=300)
def get_title_data():
    return jsonify(graph_title_data)

if __name__ == '__main__':
    app.run(debug=True)
