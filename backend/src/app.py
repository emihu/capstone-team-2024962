from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.integration import find_flights_intersecting
from astropy.time import Time, TimeDelta

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
    simulated_time = data.get('datetime')
    simulated_flights = data.get('simulatedFlights')
    
    if simulated_time == "":
        simulated_time = None
    else:
        simulated_time = Time(simulated_time)

    print("simulated time: ", type(simulated_time), simulated_time)
    flights_position, flight_data = find_flights_intersecting (focal_length, camera_sensor_size, barlow_reducer_factor, exposure, fov_center_ra_h, \
                                   fov_center_ra_m, fov_center_ra_s, fov_center_dec, longitude, latitude, altitude, flight_data_type, simulated_flights, simulated_time)

    # sample data
    # flight_data = [
    #     {
    #         "flight_number": 1234,
    #         "altitude": 35000,
    #         "heading": 90,
    #         "latitude": 43.65,
    #         "longitude": -79.38,
    #         "speed": 450,
    #         "entry": "2025-03-21T11:15:00Z",
    #         "exit": "2025-03-21T11:45:00Z",
    #     },
    #     {
    #         "flight_number": 5678,
    #         "altitude": 28000,
    #         "heading": 270,
    #         "latitude": 40.71,
    #         "longitude": -74.01,
    #         "speed": 400,
    #         "entry": "2025-03-21T12:00:00Z",
    #         "exit": "2025-03-21T12:30:00Z",
    #     },
    # ]

    # flights_position = [
    #     [{"ID": 1234, "RA": 30, "Dec": 50, "Heading": 90}, {"ID": 5678, "RA": 33, "Dec": 48, "Heading": 0}],
    #     [{"ID": 1234, "RA": 31, "Dec": 50, "Heading": 90}, {"ID": 5678, "RA": 33, "Dec": 49, "Heading": 0}],
    #     [{"ID": 1234, "RA": 32, "Dec": 50, "Heading": 90}, {"ID": 5678, "RA": 33, "Dec": 50, "Heading": 0}],
    #     [{"ID": 1234, "RA": 33, "Dec": 50, "Heading": 90}, {"ID": 5678, "RA": 33, "Dec": 51, "Heading": 0}],
    #     [{"ID": 1234, "RA": 34, "Dec": 50, "Heading": 90}, {"ID": 5678, "RA": 33, "Dec": 52, "Heading": 0}],
    #     [{"ID": 1234, "RA": 35, "Dec": 50, "Heading": 90}, {"ID": 5678, "RA": 33, "Dec": 53, "Heading": 0}],
    # ]

    #flights_position = [[{"ID": 1234, "RA": 33, "Dec": 50, "Heading": 0}], [{"ID": 1234, "RA": 33, "Dec": 50, "Heading": 0}], [{"ID": 1234, "RA": 33, "Dec": 50, "Heading": 0}]]

    flight_data = [flight.to_dict() for flight in flight_data]

    return jsonify({
        "flights_position": flights_position,
        "flight_data": flight_data
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)