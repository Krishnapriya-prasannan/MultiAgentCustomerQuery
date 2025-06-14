from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

app = Flask(__name__)
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Base prompt for generating resolution recommendation
base_prompt = """
You are an AI assistant trained to suggest helpful and accurate resolution recommendations for banking-related customer service queries.

Your input will be a customer query.

Please provide a clear and actionable recommendation that helps resolve the issue. Keep the response under 3-4 lines.

Example:
Query: I lost my card and need to block it immediately.
Response: Please block your card via the app by selecting ‘Lost or Stolen Card’ under card settings, or call our helpline immediately to prevent misuse.

Only provide helpful resolution steps. Do not ask questions or repeat the query.
"""

def get_resolution_from_gemini(user_query):
    prompt = base_prompt + f"\nQuery: {user_query}\nResponse:"
    time.sleep(1)
    model = genai.GenerativeModel("models/gemini-2.0-flash-001")
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/recommend-resolution", methods=["POST"])
def recommend_resolution():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    recommendation = get_resolution_from_gemini(query)

    return jsonify({
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
