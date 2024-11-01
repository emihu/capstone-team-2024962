### Functions that interact with the flight API ###

## API documentation: https://jeanextreme002.github.io/FlightRadarAPI/
## Note: Coordinates are in the format (latitude, longitude). Latitude is y, longitude is x. Positive is east/north, negative is west/south. E.g. Toronto's coordinates are (43.7, -79.42).

from FlightRadar24 import FlightRadar24API

# Given a list of flight objects obtained from calling the FR24 API, 
# return a list of dictionaries with the flight's flight number, coordinates, altitude, speed, and heading
def get_flight_info(flights):
    flight_info = []
    for flight in flights:
        flight_info.append({
            "flight_number": flight.flight_number,
            "coordinates": flight.coordinates,
            "altitude": flight.altitude,
            "speed": flight.speed,
            "heading": flight.heading
        })
    return flight_info


# Given the min and max lat/lon points of a rectangle, 
# return all flights that are within that rectangle along with their coordinates, altitude, speed, and heading
def find_flights_in_rect_boundary(min_lon, min_lat, max_lon, max_lat):
    fr_api = FlightRadar24API()
    bounds = f"{max_lat},{min_lat},{min_lon},{max_lon}" #north, south, west, east
    flights = fr_api.get_flights(bounds=bounds)
    return get_flight_info(flights)


# Given a lat/lon point and a radius in meters, 
# return all flights that are within that radius of that point
def find_flights_in_circ_boundary(lat, lon, radius):
    fr_api = FlightRadar24API()
    bounds = fr_api.get_bounds_by_point(lat, lon, radius)
    flights = fr_api.get_flights(bounds=bounds)
    return get_flight_info(flights)