"""Draws the complete scenes to the matrix
"""
from datetime import datetime
import json
import logging
import os.path
import time
from components.drawing import (
    draw_aircraft_details,
    draw_clock,
    draw_flight_details,
    draw_horizontal_line,
    draw_stats,
)
from components import config
import components.theme

logger = logging.getLogger(__name__)

def scene_clock(matrix, canvas):
    """Displays the clock scene

    Args:
        matrix (_type_): Matrix to display on
        canvas (_type_): Canvas to display
    """
    draw_clock(canvas, components.theme.font)
    matrix.SwapOnVSync(canvas)
    time.sleep(1)

def scene_flight_tracker(matrix, canvas, data, flight_counter, offset, text):
    """Displays the flight tracker scene

    Args:
        matrix (_type_): Matrix to display on
        canvas (_type_): Canvas to display
    """
    draw_flight_details(canvas, components.theme.font, components.theme.font_small, data, flight_counter)
    draw_horizontal_line(canvas)
    draw_aircraft_details(canvas, components.theme.font, offset, text)
    matrix.SwapOnVSync(canvas)
    return offset - 1

def scene_stats(matrix, canvas):
    """Displays the stats scene

    Args:
        matrix (_type_): Matrix to display on
        canvas (_type_): Canvas to display
    """
    today_date = datetime.now().strftime("%Y%m%d")
    flight_count = '0'

    if os.path.getsize(config.config_dict['Logging']['historical_data']) > 0:
        with open(config.config_dict['Logging']['historical_data'], "r", encoding="utf-8") as f:
            data = json.load(f)
        flight_count = str(len(data[today_date]))

    logger.info('Flights seen so far today - %s', flight_count)

    canvas.Clear()
    draw_stats(canvas, components.theme.font, flight_count)
    matrix.SwapOnVSync(canvas)
    time.sleep(10)
