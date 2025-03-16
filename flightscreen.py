#!/usr/bin/env python3

from datetime import datetime
import time #TODO remove this
from rgbmatrix import graphics
from components.matrix_control import setUpMatrix
from components.drawing import draw_horizontal_line, draw_flight_details
from components.api import repoll_flight_api, get_local_flights
import config

# Vars
LAST_FLIGHT_POLL_TIMESTAMP = datetime.now()
FLIGHT_COUNTER = 0

matrix, canvas = setUpMatrix()

# Load a font
font = graphics.Font()
font.LoadFont(config.FONT_REGULAR)

font_small = graphics.Font()
font_small.LoadFont(config.FONT_SMALL)


# Design Vars
TEXT_COLOR_MAIN = graphics.Color(0, 255, 0)
FLIGHT_DETAILS_POSITION = (3, 11)

# Initial offset
offset = matrix.width


parsed_data = []
plane_position = (5, 12 + config.PIXEL_HEIGHT / 2)



LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = get_local_flights()

# parsed_data = {'airport_origin': 'GVA', 'airport_destination': 'EDI', 'plane_make': 'Airbus', 'plane_model': 'A320'}
# parsed_data = []

while True:

    canvas.Clear()

    if len(parsed_data) == 0:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        graphics.DrawText(
            canvas,
            font,
            (config.PIXEL_WIDTH - 48) // 2, #TODO support other font sizes
            11,
            TEXT_COLOR_MAIN,
            current_time
        )
        matrix.SwapOnVSync(canvas)
        time.sleep(1)

        print(f'Poll - {LAST_FLIGHT_POLL_TIMESTAMP}')
        LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = repoll_flight_api(parsed_data, LAST_FLIGHT_POLL_TIMESTAMP)


    else:
        draw_flight_details(canvas, font, font_small, parsed_data, FLIGHT_COUNTER, TEXT_COLOR_MAIN)

        graphics.DrawText(canvas, font_small, 50, 11, TEXT_COLOR_MAIN, f'{FLIGHT_COUNTER+1}/{len(parsed_data)}')

        draw_horizontal_line(canvas)

        plane_details_text = f"{parsed_data[FLIGHT_COUNTER]['plane_make']} {parsed_data[FLIGHT_COUNTER]['plane_model']}"
        text_width = font.CharacterWidth(ord(plane_details_text[0])) * len(plane_details_text)

        graphics.DrawText(canvas, font, offset, 12 + config.PIXEL_HEIGHT/2, TEXT_COLOR_MAIN, plane_details_text)
        matrix.SwapOnVSync(canvas)
        offset -= 1  # Scroll to the left

        # Wrap around
        if offset + text_width < 0:
            offset = matrix.width
            FLIGHT_COUNTER = (FLIGHT_COUNTER + 1) % len(parsed_data)

            if FLIGHT_COUNTER == 0:
                LAST_FLIGHT_POLL_TIMESTAMP, parsed_data = repoll_flight_api(parsed_data, LAST_FLIGHT_POLL_TIMESTAMP)

        time.sleep(config.SCROLL_SPEED)  # Adjust scrolling speed

# Display the canvas
matrix.SwapOnVSync(canvas)

# Optional delay
time.sleep(5)

# Clear the canvas
canvas.Clear()
matrix.SwapOnVSync(canvas)
