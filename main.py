from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai

# Set up OpenAI API key (Replace with your actual key)
openai.api_key = "your-api-keygit "

# Initialize Flask app
app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/chatgpt"
try:
    mongo = PyMongo(app)
    print("Connected to MongoDB successfully.")
except Exception as e:
    print("Error connecting to MongoDB:", e)

@app.route("/")
def home():
    """Renders the home page with existing chats from MongoDB."""
    try:
        # Fetch chats from the MongoDB collection
        chats = mongo.db.chats.find({})
        myChats = [chat for chat in chats]
        print("Chats fetched from DB:", myChats)
        return render_template("index.html", myChats=myChats)
    except Exception as e:
        print("Error fetching chats from MongoDB:", e)
        return render_template("index.html", myChats=[])

@app.route("/api", methods=["POST"])
def qa():
    """Handles Q&A interactions."""
    if request.method == "POST":
        try:
            # Parse incoming JSON request
            data = request.json
            print("Received JSON data:", data)

            if not data or "question" not in data:
                return jsonify({"error": "Invalid request. 'question' field is required."}), 400

            question = data["question"].strip()
            if not question:
                return jsonify({"error": "The 'question' field cannot be empty."}), 400

            # Check if the question exists in the database
            chat = mongo.db.chats.find_one({"question": question})
            if chat:
                print("Answer found in DB:", chat)
                return jsonify({"question": question, "answer": chat["answer"]})

            # Call OpenAI API for a new answer
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",  # Updated to a valid OpenAI model
                prompt=question,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            print("OpenAI Response:", response)

            # Extract the answer and insert it into the database
            answer = response["choices"][0]["text"].strip()
            mongo.db.chats.insert_one({"question": question, "answer": answer})
            return jsonify({"question": question, "answer": answer})

        except Exception as e:
            print("Error in QA endpoint:", e)
            return jsonify({"error": "An error occurred while processing your request."}), 500

# Default fallback for unhandled routes
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
