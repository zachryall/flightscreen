"""Component functions
"""
from datetime import datetime
import json
import logging
import os.path
from FlightRadar24 import FlightRadar24API
import components.config

logger = logging.getLogger(__name__)

fr_api = FlightRadar24API()

def repoll_flight_api(parsed_data, last_poll_timestamp):
    if last_poll_timestamp == 0:
        last_poll_timestamp, parsed_data = get_local_flights()
    else:
        now_timestamp = datetime.now()
        elapsed_time = (now_timestamp - last_poll_timestamp).total_seconds()
        if elapsed_time > components.config.config_dict['Display']['repoll_time']:
            last_poll_timestamp, parsed_data = get_local_flights()
    return last_poll_timestamp, parsed_data

def get_local_flights():
    bounds = fr_api.get_bounds_by_point(
        float(components.config.config_dict['Location']['lat']), #TODO is there a better way
        float(components.config.config_dict['Location']['long']),
        int(components.config.config_dict['Location']['radius'])
    )
    flights_local = fr_api.get_flights(bounds = bounds)

    logger.info('Flights found: %s' % len(flights_local))

    parsed_data = []
    for flight_local in flights_local:

        flight_details = fr_api.get_flight_details(flight_local)

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

        aircraft_data = {
            "airport_origin": airport_origin,
            "airport_destination": airport_destination,
            "plane_make": flight_details['aircraft']['model']['text'].split(' ')[0],
            "plane_model": flight_details['aircraft']['model']['code'],
            "flight_number": flight_details['identification']['number']['default'],
        }

        # Add the aircraft data to the list
        parsed_data.append(aircraft_data)

        today_date = datetime.now().strftime("%Y%m%d")

        if os.path.getsize(components.config.config_dict['Logging']['historical_data']) > 0:
            with open(components.config.config_dict['Logging']['historical_data'], "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        if today_date not in data:
            data[today_date] = []

        if aircraft_data['flight_number'] not in data[today_date]:
            data[today_date].append(aircraft_data['flight_number'])

        with open(components.config.config_dict['Logging']['historical_data'], "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    logger.debug(parsed_data)
    return datetime.now(), parsed_data
