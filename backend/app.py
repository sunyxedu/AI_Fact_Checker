from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
import os
from dotenv import load_dotenv
from urllib.parse import unquote

from main import get_app_data, AppData

# Set your OpenAI API key
app = Flask(__name__)
CORS(app)


app_data: AppData = None


# Configure cache
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',  # Use 'redis' for production
    'CACHE_DEFAULT_TIMEOUT': None  # 5 minutes
})


load_dotenv()  # Load .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.route('/misinformation/<path:youtube_url>')
@cache.cached(timeout=None)
def get_misinformation(youtube_url: str):
    decoded_url = unquote(youtube_url)
    app_data = get_app_data(decoded_url)
    return jsonify(app_data.misinformation_graph)


@app.route("/statement/<int:misinformation_id>")
@cache.cached(timeout=None)
def get_statements(misinformation_id: int):
    return jsonify(app_data.statement_graphs[misinformation_id])


@app.route("/provenance/<int:statement_id>")
@cache.cached(timeout=None)
def get_provenance(statement_id: int):
    return jsonify(app_data.article_dagraph[statement_id])


@app.route("/video_url")
@cache.cached(timeout=None)
def get_video_url():
    return jsonify(app_data.url)


if __name__ == '__main__':
    app.run(debug=True)
