from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/", methods=['GET'])
def home ():
    return "hello world"

@app.route("/api/flight-prediction", methods=['GET'])
def flightPrediction ():
    return jsonify(
        {
            "interference": True
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=8080)