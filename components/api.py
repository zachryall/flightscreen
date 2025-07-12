"""Component functions
"""
from datetime import datetime
import logging
import os.path
from FlightRadar24 import FlightRadar24API
from components.utils import get_config
from components.db import insert_airline, insert_airport, insert_flight, insert_plane_model, insert_plane_registration
logger = logging.getLogger(__name__)
fr_api = FlightRadar24API()
hide_unknown = get_config('Location', 'hide_flights_with_missing_data')
allowed_plane_manufacters = get_config('Location', 'allowed_plane_manufacters')
disallowed_airlines = get_config('Location', 'disallowed_airlines')

def repoll_flight_api(parsed_data, last_poll_timestamp):
    """Polls the api for flight information

    Args:
        parsed_data (dict): Retrieved data
        last_poll_timestamp (string): Timestamp of the last poll

    Returns:
        _type_: _description_
    """
    if last_poll_timestamp == 0:
        last_poll_timestamp, parsed_data = get_local_flights()
    else:
        now_timestamp = datetime.now()
        elapsed_time = (now_timestamp - last_poll_timestamp).total_seconds()
        if elapsed_time > get_config('Display', 'repoll_time'):
            last_poll_timestamp, parsed_data = get_local_flights()
    return last_poll_timestamp, parsed_data

def get_local_flights():
    """Retrives the details of flights in the defined area

    Returns:
        tuple: timestamp of the request, retrieved data dict
    """
    bounds = fr_api.get_bounds_by_point(
        float(get_config('Location', 'lat')),
        float(get_config('Location', 'long')),
        get_config('Location', 'radius')
    )
    try:
        flights_local = fr_api.get_flights(bounds = bounds)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    logger.info('Flights found: %s', len(flights_local))

    parsed_data = []
    for flight_local in flights_local:

        try:
            flight_details = fr_api.get_flight_details(flight_local)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        #defaults
        airport_origin = ' ? '
        airport_destination = ' ? '

        try:
            airport_origin = flight_details['airport']['origin']['code']['iata']
        except TypeError:
            logger.debug('No origin found')
        try:
            airport_destination = flight_details['airport']['destination']['code']['iata']
        except TypeError:
            logger.debug('No destination found')

        try:
            plane_make = flight_details['aircraft']['model']['text'].split(' ')[0]
        except TypeError:
            logger.debug = ('Flight with aircraft info found')
        
        airline = None
        try:
            airline = flight_details['airline']['name']
        except TypeError:
            logger.debug = ('Flight with no airline found')
        print('1')
        if (hide_unknown 
            and airport_origin != airport_destination != ' ? '
            and plane_make.lower() in allowed_plane_manufacters
            and airline.lower() not in disallowed_airlines
            and airline):

            today_date = datetime.now().strftime("%Y%m%d")

            aircraft_data = {
                "airport_origin_iata": airport_origin,
                "airport_origin_name": flight_details['airport']['origin']['name'],
                "airport_origin_country": flight_details['airport']['origin']['position']['country']['name'],
                "airport_origin_lat": flight_details['airport']['origin']['position']['latitude'],
                "airport_origin_long": flight_details['airport']['origin']['position']['longitude'],
                "airport_destination_iata": airport_destination,
                "airport_destination_name": flight_details['airport']['destination']['name'],
                "airport_destination_country": flight_details['airport']['destination']['position']['country']['name'],
                "airport_destination_lat": flight_details['airport']['destination']['position']['latitude'],
                "airport_destination_long": flight_details['airport']['destination']['position']['longitude'],
                "plane_make": plane_make,
                "plane_model": flight_details['aircraft']['model']['code'],
                "flight_number": flight_details['identification']['number']['default'],
                "airline": airline,
                "tail_number": flight_details['aircraft']['registration'],
                "date": today_date
            }

            insert_airport(aircraft_data)
            insert_airline(aircraft_data)
            insert_plane_model(aircraft_data)
            insert_plane_registration(aircraft_data)
            insert_flight(aircraft_data)
            parsed_data.append(aircraft_data)

    return datetime.now(), parsed_data
