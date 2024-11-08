from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.fov import check_flights_in_fov

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/", methods=['GET'])
def home ():
    return "hello world"

@app.route("/api/flight-prediction", methods=['POST'])
def flightPrediction():
    data = request.json
    focal_length = float(data.get('focal_length'))
    camera_sensor_size = float(data.get('camera_sensor_size'))
    barlow_reducer_factor = float(data.get('barlow_reducer_factor'))
    fov_center_ra = float(data.get('fov_center_ra'))
    fov_center_dec = float(data.get('fov_center_dec'))
    
    result = check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, fov_center_ra, fov_center_dec)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8080)