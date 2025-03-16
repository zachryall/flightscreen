"""Component functions
"""
from datetime import datetime
import config
from FlightRadar24 import FlightRadar24API


fr_api = FlightRadar24API()

def repoll_flight_api(parsed_data, last_poll_timestamp):
    if last_poll_timestamp == 0:
        last_poll_timestamp, parsed_data = get_local_flights()
    else:
        now_timestamp = datetime.now()
        elapsed_time = (now_timestamp - last_poll_timestamp).total_seconds()
        if elapsed_time > config.REPOLL_TIME:
            last_poll_timestamp, parsed_data = get_local_flights()
    return last_poll_timestamp, parsed_data 

def get_local_flights():
    bounds = fr_api.get_bounds_by_point(config.LAT, config.LONG, config.RADIUS)
    flights_local = fr_api.get_flights(bounds = bounds)

    for flight_local in flights_local:
        parsed_data = []

        flight_details = fr_api.get_flight_details(flight_local)

        #defaults
        airport_origin = ' ? '
        airport_destination = ' ? '

        try:
            airport_origins = flight_details['airport']['origin']['code']['iata']
        except TypeError:
            print('No origin')
        try:
            airport_destination = flight_details['airport']['destination']['code']['iata']
        except TypeError:
            print('No destination')

        aircraft_data = {
            "airport_origin": airport_origin,
            "airport_destination": airport_destination,
            "plane_make": flight_details['aircraft']['model']['text'].split(' ')[0],
            "plane_model": flight_details['aircraft']['model']['code'],
        }

    print(aircraft_data)

    # Add the aircraft data to the list
    parsed_data.append(aircraft_data)
    return datetime.now(), parsed_data
