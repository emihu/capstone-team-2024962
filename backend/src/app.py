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
    print("here:", data)

    focal_length = float(data.get('focalLength'))
    camera_sensor_size = float(data.get('cameraSensorSize'))
    barlow_reducer_factor = float(data.get('barlowReducerFactor'))
    fov_center_ra_h = float(data.get('fovCenterRaH'))
    fov_center_ra_m = float(data.get('fovCenterRaM'))
    fov_center_ra_s = float(data.get('fovCenterRaS'))
    fov_center_dec = float(data.get('fovCenterDec'))
    flight_data_type = data.get('flightDataType')
    simulated_flights = data.get('simulatedFlights')
    
    result = check_flights_in_fov(focal_length, camera_sensor_size, barlow_reducer_factor, fov_center_ra_h, \
                                  fov_center_ra_m, fov_center_ra_s, fov_center_dec, flight_data_type, simulated_flights)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)