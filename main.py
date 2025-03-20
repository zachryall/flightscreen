"""Main file
"""
from datetime import datetime
import logging
import os.path
import sys
import time
from components.api import repoll_flight_api, get_local_flights
from components.matrix_control import set_up_matrix
from components import config
import components.theme
from components.scene import scene_clock, scene_flight_tracker, scene_stats

def main():
    """Main function
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

    if config.config_dict['Logging']['debug_mode']:
        logging.basicConfig(
            level=logging.DEBUG
        )

    logger = logging.getLogger(__name__)
    logger.info('The script has started')

    # Vars
    flight_counter = 0

    matrix, canvas = set_up_matrix()

    # Initial offset
    offset = matrix.width


    parsed_data = []

    if not os.path.exists(config.config_dict['Logging']['historical_data']):
        logger.error('No ./historical_data.json file')
        sys.exit()


    last_flight_poll_timestamp, parsed_data = get_local_flights()

    while True:

        canvas.Clear()

        night_start = datetime.strptime(config.config_dict['Display']['night_time_start'], "%H:%M").time()
        night_end = datetime.strptime(config.config_dict['Display']['night_time_end'], "%H:%M").time()
        current_time = datetime.now().time()

        if night_start <= current_time or current_time <= night_end:
            print('In night-time mode, trying again in 60secs')
            logger.debug('In night-time mode, trying again in %s', config.config_dict['Display']['repoll_time'])
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

            time.sleep(config.config_dict['Display']['scroll_speed'])

if __name__ == '__main__':
    main()
