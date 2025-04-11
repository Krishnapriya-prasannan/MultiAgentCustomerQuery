from flask import Flask, request, jsonify
from flask_cors import CORS
from db import collection
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Customer Query API running"

@app.route("/submit", methods=["POST"])
def submit_query():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not all([name, email, message]):
        return jsonify({"error": "Missing fields"}), 400

    query = {
        "name": name,
        "email": email,
        "message": message,
        "createdAt": datetime.utcnow(),
        "__v": 0
    }

    result = collection.insert_one(query)
    return jsonify({"message": "Query submitted", "id": str(result.inserted_id)})

if __name__ == "__main__":
    app.run(debug=True)
