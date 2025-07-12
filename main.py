"""Main file
"""
from datetime import datetime
import logging
import os.path
import sys
import time
import sqlite3
from components.api import repoll_flight_api, get_local_flights
from components.matrix_control import set_up_matrix
from components.utils import get_config
import components.theme
from components.scene import scene_boot, scene_clock, scene_flight_tracker, scene_stats
from components.db import create_table

def main():
    """Main function
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    if get_config('Logging', 'debug_mode'):
        logging.basicConfig(
            level=logging.DEBUG
        )

    logger = logging.getLogger(__name__)
    logger.debug('The script has started')

    # Vars
    flight_counter = 0
    night_start = datetime.strptime(get_config('Display', 'night_time_start'), "%H:%M").time()
    night_end = datetime.strptime(get_config('Display', 'night_time_end'), "%H:%M").time()
    scroll_speed = float(get_config('Display', 'scroll_speed'))

    matrix, canvas = set_up_matrix()
    offset = matrix.width

    parsed_data = []

    if not os.path.exists('./historical_data.json'):
        logger.error('No ./historical_data.json file')
        sys.exit()

    # Update this check to the new database path
    DB_FILE_PATH_MAIN = '/var/lib/flightscreen/flights.db' # Define it here as well for the check
    if not os.path.exists(DB_FILE_PATH_MAIN):
        logger.info(f'No .db file found at {DB_FILE_PATH_MAIN}')
        try:
            create_table() # This will now create it at /var/lib/flightscreen/flights.db
        except Exception as e:
            logger.error(f"Failed to create database table: {e}")
            sys.exit(1) # Exit if database creation fails critically

    if get_config('Display', 'show_ip_on_boot'):
        scene_boot(matrix,canvas)

    last_flight_poll_timestamp, parsed_data = get_local_flights()

    while True:

        canvas.Clear()

        current_time = datetime.now().time()

        if night_start <= current_time or current_time <= night_end:
            print('In night-time mode, trying again in 60secs')
            logger.debug('In night-time mode, trying again in %s', get_config('Display', 'repoll_time'))
            time.sleep(60)
        elif len(parsed_data) == 0:
            scene_clock(matrix, canvas)
            last_flight_poll_timestamp, parsed_data = repoll_flight_api(parsed_data, last_flight_poll_timestamp)
        else:
            plane_details_text = f"{parsed_data[flight_counter]['plane_make']} {parsed_data[flight_counter]['plane_model']}"
            text_width = components.theme.font.CharacterWidth(ord(plane_details_text[0])) * len(plane_details_text)
            offset = scene_flight_tracker(matrix, canvas, parsed_data, flight_counter, offset, plane_details_text)

            # Wrap around
            if offset + text_width < 0:
                offset = matrix.width
                flight_counter = (flight_counter + 1) % len(parsed_data)

                if flight_counter == 0:
                    scene_stats(matrix, canvas)
                    last_flight_poll_timestamp, parsed_data = repoll_flight_api(parsed_data, last_flight_poll_timestamp)

            time.sleep(scroll_speed)

if __name__ == '__main__':
    main()
