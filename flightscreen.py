#!/usr/bin/env python3

from datetime import datetime
import json
import logging
import os.path
import sys
import time
from rgbmatrix import graphics
from components.api import repoll_flight_api, get_local_flights
from components.drawing import (
    draw_aircraft_details,
    draw_clock,
    draw_flight_details,
    draw_horizontal_line,
    draw_stats,
)
from components.matrix_control import set_up_matrix
import components.theme
import config


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

if config.DEBUG_MODE:
    logging.basicConfig(
        level=logging.DEBUG
    )

logger = logging.getLogger(__name__)

logger.info('The script has started')

# Vars
LAST_FLIGHT_POLL_TIMESTAMP = datetime.now()
FLIGHT_COUNTER = 0

matrix, canvas = set_up_matrix()

# Design Vars

FLIGHT_DETAILS_POSITION = (3, 11)

# Initial offset
offset = matrix.width


parsed_data = []


if not os.path.exists(config.HISTORICAL_DATA):
    logger.error('No ./historical_data.json file')
    sys.exit()


LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = get_local_flights()

while True:

    canvas.Clear()

    if len(parsed_data) == 0:
        draw_clock(canvas, components.theme.font)
        matrix.SwapOnVSync(canvas)
        time.sleep(1)

        logger.info('Poll - %s' % LAST_FLIGHT_POLL_TIMESTAMP)
        LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = repoll_flight_api(parsed_data, LAST_FLIGHT_POLL_TIMESTAMP)


    else:
        plane_details_text = f"{parsed_data[FLIGHT_COUNTER]['plane_make']} {parsed_data[FLIGHT_COUNTER]['plane_model']}"
        text_width = components.theme.font.CharacterWidth(ord(plane_details_text[0])) * len(plane_details_text)

        draw_flight_details(canvas, components.theme.font, components.theme.font_small, parsed_data, FLIGHT_COUNTER)
        draw_horizontal_line(canvas)
        draw_aircraft_details(canvas, components.theme.font, offset, plane_details_text)

        matrix.SwapOnVSync(canvas)
        offset -= 1  # Scroll to the left

        # Wrap around
        if offset + text_width < 0:
            offset = matrix.width
            FLIGHT_COUNTER = (FLIGHT_COUNTER + 1) % len(parsed_data)

            if FLIGHT_COUNTER == 0:
                today_date = datetime.now().strftime("%Y%m%d")

                if os.path.getsize(config.HISTORICAL_DATA) > 0:
                    with open(config.HISTORICAL_DATA, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    FLIGHT_COUNT = str(len(data[today_date]))
                else:
                    FLIGHT_COUNT = '0'
                logger.info('Flights seen so far today - %s' % FLIGHT_COUNT)

                canvas.Clear()
                draw_stats(canvas, components.theme.font, FLIGHT_COUNT)
                matrix.SwapOnVSync(canvas)
                time.sleep(10)

                LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = repoll_flight_api(parsed_data, LAST_FLIGHT_POLL_TIMESTAMP)

        time.sleep(config.SCROLL_SPEED)  # Adjust scrolling speed

# Display the canvas
matrix.SwapOnVSync(canvas)

# Optional delay
time.sleep(5)

# Clear the canvas
canvas.Clear()
matrix.SwapOnVSync(canvas)
