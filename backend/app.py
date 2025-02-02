from flask import Flask, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import openai

# Set your OpenAI API key
OPENAI_API_KEY = "REDACTED"
app = Flask(__name__)
CORS(app)
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
        [1, 2],
        [4, 3],
        [1, 3],
        [4, 5],
        [1, 6]
    ]
}
#LEVEL 2 IS FOR WHEN YOU CLICK ON A CATEGORY NODE FROM LEVEL 1
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
        [4, 3],
        [1, 3],
        [4, 5],
        [1, 6]
    ],
    "node_name": [
        "Quotes"
    ]
}
#LEVEL 3 IS FOR SOURCES SO YOU DONT HAVE TO ALTER SEVERITY (THIS IS UP TO CHOICE)
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

#THIS IS THE TITLE OF THE VIDEO INPUT HERE
graph_title_data = {
    "header": "Youtube Video: Trump Inauguration"
}
@app.route('/node_lvl_1', methods=['GET'])
def get_data_lvl_1():
    return jsonify(graph_data_lvl_1)

@app.route('/node_lvl_2', methods=['GET'])
def get_data_lvl_2():
    return jsonify(graph_data_lvl_2)

@app.route('/node_lvl_3', methods=['GET'])
def get_data_lvl_3():
    return jsonify(graph_data_lvl_3)

@app.route('/lvl_2_title')
def get_title_data():
    return jsonify(graph_title_data)



if __name__ == '__main__':
    app.run(debug=True)
