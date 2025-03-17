import config
from rgbmatrix import graphics
from datetime import datetime

TEXT_COLOR_MAIN = graphics.Color(0, 255, 0) #TODO move


def draw_horizontal_line(canvas):
    DIVIDER_POSITION = (0, config.PIXEL_HEIGHT / 2)
    DIVIDER_COLOUR = graphics.Color(0, 0, 255)

    for i in range(DIVIDER_POSITION[0], DIVIDER_POSITION[0] + config.PIXEL_WIDTH):
        canvas.SetPixel(i, DIVIDER_POSITION[1], DIVIDER_COLOUR.red, DIVIDER_COLOUR.green, DIVIDER_COLOUR.blue)

def draw_flight_details(canvas, font, font_small, parsed_data, FLIGHT_COUNTER):
    FLIGHT_DETAILS_POSITION = (3, 11)

    graphics.DrawText(
        canvas,
        font,
        FLIGHT_DETAILS_POSITION[0],
        FLIGHT_DETAILS_POSITION[1],
        TEXT_COLOR_MAIN,
        f"{parsed_data[FLIGHT_COUNTER]['airport_origin']}>{parsed_data[FLIGHT_COUNTER]['airport_destination']}"
    )
    graphics.DrawText(canvas, font_small, 50, 11, TEXT_COLOR_MAIN, f'{FLIGHT_COUNTER+1}/{len(parsed_data)}')

def draw_aircraft_details(canvas, font, offset, text):
    graphics.DrawText(canvas, font, offset, 12 + config.PIXEL_HEIGHT/2, TEXT_COLOR_MAIN, text)

def draw_clock(canvas, font):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    graphics.DrawText(
        canvas,
        font,
        (config.PIXEL_WIDTH - 48) // 2, #TODO support other font sizes
        11, #TODO centre
        TEXT_COLOR_MAIN,
        current_time
    )

def draw_stats(canvas, font, count):

    text_top = f'{count} flights'
    text_width_top = font.CharacterWidth(ord(text_top[0])) * len(text_top)
    text_bottom = 'seen today'
    text_width_bottom = font.CharacterWidth(ord(text_bottom[0])) * len(text_bottom)


    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    graphics.DrawText(
        canvas,
        font,
        (config.PIXEL_WIDTH - text_width_top) // 2, #TODO support other font sizes
        11, #TODO centre
        TEXT_COLOR_MAIN,
        text_top
    )
    graphics.DrawText(
        canvas,
        font,
        (config.PIXEL_WIDTH - text_width_bottom) // 2, #TODO support other font sizes
        12 + config.PIXEL_HEIGHT/2, #TODO centre
        TEXT_COLOR_MAIN,
        text_bottom
    )
