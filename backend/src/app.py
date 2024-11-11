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
    data = request.get_json()

    focal_length = float(data.get('focalLength'))
    camera_sensor_size = float(data.get('cameraSensorSize'))
    barlow_reducer_factor = float(data.get('barlowReducerFactor'))
    fov_center_ra = float(data.get('fovCenterRa'))
    fov_center_dec = float(data.get('fovCenterDec'))
    
    result = check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, fov_center_ra, fov_center_dec)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)