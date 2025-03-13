from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.integration import find_flights_intersecting
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
    exposure = float(data.get('exposure'))
    fov_center_ra_h = float(data.get('fovCenterRaH'))
    fov_center_ra_m = float(data.get('fovCenterRaM'))
    fov_center_ra_s = float(data.get('fovCenterRaS'))
    fov_center_dec = float(data.get('fovCenterDec'))
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))
    altitude = float(data.get('altitude'))
    flight_data_type = data.get('flightDataType')
    simulated_flights = data.get('simulatedFlights')
    
    flights_position, flight_data = find_flights_intersecting (focal_length, camera_sensor_size, barlow_reducer_factor, exposure, fov_center_ra_h, \
                                   fov_center_ra_m, fov_center_ra_s, fov_center_dec, longitude, latitude, altitude, flight_data_type, simulated_flights)

    return jsonify({
        "flights_position": flights_position,
        "flight_data": flight_data
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)