from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import google.generativeai as genai
import time

app = Flask(__name__)
load_dotenv()
CORS(app)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Summarization prompt instruction
base_prompt = """
You are a helpful assistant that summarizes user-submitted banking-related queries.
Given a customer's query, your task is to provide a brief and clear summary of the issue.
Only provide the summary and nothing else.

Examples:
Query: I made a top-up through my debit card, but the balance is not reflecting.
Summary: Top-up via debit card not reflected in balance.

Query: My card was swallowed by an ATM. What should I do?
Summary: Card swallowed by ATM.

Query: Why was I charged twice for a single transaction?
Summary: Duplicate transaction charge.

Now, summarize the following query.
"""

def get_summary_from_gemini(user_query):
    prompt = base_prompt + f"\nQuery: {user_query}\nSummary:"
    time.sleep(1)
    model = genai.GenerativeModel("models/gemini-2.0-flash-001")
    response = model.generate_content(prompt)
    return response.text.strip()

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    summary = get_summary_from_gemini(query)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
