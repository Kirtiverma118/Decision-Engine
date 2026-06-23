import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from flask import Flask, request, jsonify
from decision_engine import decide_next_action

app = Flask(__name__)


@app.route("/decide", methods=["POST"])
def decide():
    Expects JSON body:
    {
        "score": 7.5,
        "context": {
            "history": [...],
            "total_questions_asked": 3,
            "follow_up_count_on_topic": 0
        }
    }

    Returns JSON:
    {
        "action": "next_question"
    }
    data = request.get_json()
        return jsonify({"error": "Please provide 'score' in request body"}), 400

    score = data.get("score")
    context = data.get("context", {})

    result = decide_next_action(score, context)
    return jsonify(result)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Decision Engine API is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
