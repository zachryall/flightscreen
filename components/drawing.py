from datetime import datetime
from rgbmatrix import graphics
import config

TEXT_COLOR_MAIN = graphics.Color(0, 255, 0)
divider_colour = graphics.Color(0, 0, 255)


def draw_horizontal_line(canvas):
    divider_position = (0, config.PIXEL_HEIGHT / 2)

    for i in range(divider_position[0], divider_position[0] + config.PIXEL_WIDTH):
        canvas.SetPixel(i, divider_position[1], divider_colour.red, divider_colour.green, divider_colour.blue)

def draw_flight_details(canvas, font, font_small, parsed_data, flight_counter):
    flight_details_position = (3, 11)

    graphics.DrawText(
        canvas,
        font,
        flight_details_position[0],
        flight_details_position[1],
        TEXT_COLOR_MAIN,
        f"{parsed_data[flight_counter]['airport_origin']}>{parsed_data[flight_counter]['airport_destination']}"
    )
    graphics.DrawText(canvas, font_small, 50, 11, TEXT_COLOR_MAIN, f'{flight_counter+1}/{len(parsed_data)}')

def draw_aircraft_details(canvas, font, offset, text):
    graphics.DrawText(canvas, font, offset, 12 + config.PIXEL_HEIGHT/2, TEXT_COLOR_MAIN, text)

def draw_clock(canvas, font):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    graphics.DrawText(
        canvas,
        font,
        (config.PIXEL_WIDTH - 48) // 2,
        11,
        TEXT_COLOR_MAIN,
        current_time
    )

def draw_stats(canvas, font, count):

    text_top = f'{count} flights'
    text_width_top = font.CharacterWidth(ord(text_top[0])) * len(text_top)
    text_bottom = 'seen today'
    text_width_bottom = font.CharacterWidth(ord(text_bottom[0])) * len(text_bottom)

    graphics.DrawText(
        canvas,
        font,
        (config.PIXEL_WIDTH - text_width_top) // 2,
        11,
        TEXT_COLOR_MAIN,
        text_top
    )
    graphics.DrawText(
        canvas,
        font,
        (config.PIXEL_WIDTH - text_width_bottom) // 2,
        12 + config.PIXEL_HEIGHT/2,
        TEXT_COLOR_MAIN,
        text_bottom
    )
