from flask import Flask, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import pyautogui
import time


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



def get_transcript(video_id):
    data = []
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    for entry in transcript:
        text = entry["text"]
        timestamp = entry["start"]
        time = str(int(timestamp // 60)) + ":" + str(round(timestamp % 60))
        data.append((time, text))
    print(data)
    return data

def getFlag(sentence):
    return True

def fact_check_sentence(sentence):
    flag = getFlag(sentence)
    return flag


@app.route('/factcheck', methods=['GET'])
def factcheck():
    sentence = get_transcript("dEQfBs59G3k")
    misInformation = fact_check_sentence(sentence)
    return jsonify({"is_misinformation": misInformation}), 200, {'Content-Type': 'application/json'}

def stops():
    timestamps_in_seconds = [t[0] * 60 + t[1] for t in timestamps]
    start_time = time.time()
    for timestamp in timestamps_in_seconds:
        while time.time() - start_time < timestamp:
            time.sleep(0.1)  # Sleep to prevent high CPU usage
        pyautogui.press('space')  # Press backspace at the specified time


if __name__ == '__main__':
    app.run(debug=True)
