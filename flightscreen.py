#!/usr/bin/env python3

from datetime import datetime
import time
from rgbmatrix import graphics
from components.matrix_control import setUpMatrix
from components.drawing import draw_horizontal_line, draw_flight_details, draw_aircraft_details, draw_stats, draw_clock
from components.api import repoll_flight_api, get_local_flights
import config
import components.theme
import os.path
import sys
import logging
import json


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

matrix, canvas = setUpMatrix()

# Design Vars

FLIGHT_DETAILS_POSITION = (3, 11)

# Initial offset
offset = matrix.width


parsed_data = []


if not os.path.exists(config.HISTORICAL_DATA):
    logger.error(f'No ./historical_data.json file')
    sys.exit()


LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = get_local_flights()

# parsed_data = {'airport_origin': 'GVA', 'airport_destination': 'EDI', 'plane_make': 'Airbus', 'plane_model': 'A320'}
# parsed_data = []

while True:

    canvas.Clear()

    if len(parsed_data) == 0:
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # graphics.DrawText(
        #     canvas,
        #     components.theme.font,
        #     (config.PIXEL_WIDTH - 48) // 2, #TODO support other font sizes
        #     11,
        #     TEXT_COLOR_MAIN,
        #     current_time
        # )
        draw_clock(canvas, components.theme.font)
        matrix.SwapOnVSync(canvas)
        time.sleep(1)

        logger.info(f'Poll - {LAST_FLIGHT_POLL_TIMESTAMP}')
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
                    with open(config.HISTORICAL_DATA, "r") as f:
                        data = json.load(f)
                    flight_count = str(len(data[today_date]))
                else:
                    flight_count = '0'
                logger.info(f'Flights seen so far today - {flight_count}')
                
                canvas.Clear()
                draw_stats(canvas, components.theme.font, flight_count)
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
