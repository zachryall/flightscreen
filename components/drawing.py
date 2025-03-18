"""Functions relating to drawing to the canvas
"""
from datetime import datetime
from rgbmatrix import graphics
from components import config

TEXT_COLOR_MAIN = graphics.Color(0, 255, 0)
divider_colour = graphics.Color(0, 0, 255)


def draw_horizontal_line(canvas):
    """Draw a horizontal line to the canvas

    Args:
        canvas (_type_): Canvas to draw to
    """
    divider_position = (0, config.config_dict['Hardware']['pixel_height'] / 2)

    for i in range(
        divider_position[0],
        divider_position[0] + config.config_dict['Hardware']['pixel_width']
    ):
        canvas.SetPixel(
            i,
            divider_position[1],
            divider_colour.red,
            divider_colour.green,
            divider_colour.blue
        )

def draw_flight_details(canvas, font_details, font_counter, parsed_data, flight_counter):
    """Draw the flight's origin and destination to the canvas,
       along with the flight counter

    Args:
        canvas (_type_): Canvas to draw to
        font_details (str): Font to use for the flight details
        font_counter (str): Font to use for the flight counter
        parsed_data (dict): Data to display
        flight_counter (int): The current value of the flight counter
    """
    flight_details_position = (3, 11)

    graphics.DrawText(
        canvas,
        font_details,
        flight_details_position[0],
        flight_details_position[1],
        TEXT_COLOR_MAIN,
        f"{parsed_data[flight_counter]['airport_origin']}>{parsed_data[flight_counter]['airport_destination']}"
    )
    graphics.DrawText(
        canvas,
        font_counter,
        50,
        11,
        TEXT_COLOR_MAIN,
        f'{flight_counter+1}/{len(parsed_data)}'
    )

def draw_aircraft_details(canvas, font, offset, text):
    """Draws the make and model of the aircraft to the canvas

    Args:
        canvas (_type_): Canvas to draw to
        font (str): Font of the details
        offset (int): Offset to control the ticker style display
        text (str): Text to display
    """
    graphics.DrawText(
        canvas,
        font,
        offset,
        12 + config.config_dict['Hardware']['pixel_height']/2,
        TEXT_COLOR_MAIN,
        text
    )

def draw_clock(canvas, font):
    """Draws a clock to the canvas

    Args:
        canvas (_type_): Canvas to draw to
        font (str): Font of the clock
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    graphics.DrawText(
        canvas,
        font,
        (config.config_dict['Hardware']['pixel_width'] - 48) // 2,
        11,
        TEXT_COLOR_MAIN,
        current_time
    )

def draw_stats(canvas, font, count):
    """Draws the historical flight stats to the canvas

    Args:
        canvas (_type_): Canvas to draw to
        font (str): Font to use
        count (int): The count of flights seen
    """

    text_top = f'{count} flights'
    text_width_top = font.CharacterWidth(ord(text_top[0])) * len(text_top)
    text_bottom = 'seen today'
    text_width_bottom = font.CharacterWidth(ord(text_bottom[0])) * len(text_bottom)

    graphics.DrawText(
        canvas,
        font,
        (config.config_dict['Hardware']['pixel_width'] - text_width_top) // 2,
        11,
        TEXT_COLOR_MAIN,
        text_top
    )
    graphics.DrawText(
        canvas,
        font,
        (config.config_dict['Hardware']['pixel_width'] - text_width_bottom) // 2,
        12 + config.config_dict['Hardware']['pixel_height']/2,
        TEXT_COLOR_MAIN,
        text_bottom
    )
