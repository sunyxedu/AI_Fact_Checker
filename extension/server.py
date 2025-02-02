from flask import Flask, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import pyautogui
import time
import request
from backend.statement_extractor import extract_statements
from backend.fact_checker import fact_check
from backend.severity_checker import check_severity
from backend.statement_aggregator import aggregate_statements
import threading

# Set your OpenAI API key
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
@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    try:
        data = request.json
        video_url = data.get('video_url')
        
        if not video_url:
            return jsonify({"error": "No video URL provided"}), 400

        statements = extract_statements(video_url)
        if not statements:
            return jsonify({"error": "No statements found"}), 404

        # 2. 获取真实性分数
        truth_scores = fact_check(statements)

        # 3. 获取严重性分数
        severity_results = check_severity(statements, [])  # 空列表作为 article 参数
        severity_scores = [result[0] for result in severity_results]  # 获取每个结果的第一个元素（severity score）

        # 4. 聚合结果
        global current_misinformation_list
        current_misinformation_list = aggregate_statements(statements, truth_scores, severity_scores)

        # 5. 返回结果摘要
        result_summary = []
        timestamps = []
        for misinfo in current_misinformation_list:
            timestamps.extend([stmt.timestamp for stmt in misinfo.statements])
            result_summary.append({
                "summary": misinfo.summary,
                "severity": misinfo.severity,
                "truthiness": misinfo.truthiness,
                "timestamps": [stmt.timestamp for stmt in misinfo.statements]
            })

        # Start a new thread to handle the stops
        stop_thread = threading.Thread(target=stops, args=(timestamps,))
        stop_thread.start()

        return jsonify({
            "message": "Analysis complete",
            "results": result_summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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

def fact_check_sentence(sentence):
    return True


@app.route('/factcheck', methods=['GET'])
def factcheck():
    
    return jsonify({"is_misinformation": True}), 200, {'Content-Type': 'application/json'}

def stops(timestamps):
    for timestamp in timestamps:
        # Wait until timestamp
        time.sleep(timestamp)
        # Pause video
        pyautogui.press('space')
        # Wait 2 seconds
        time.sleep(2)
        # Resume video
        pyautogui.press('space')


if __name__ == '__main__':
    
    app.run(debug=True)
