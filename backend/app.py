from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp

app = Flask(__name__)
CORS(app)
from flask import send_from_directory
import os

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)