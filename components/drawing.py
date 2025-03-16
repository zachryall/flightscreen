import config
from rgbmatrix import graphics


def draw_horizontal_line(canvas):
    DIVIDER_POSITION = (0, config.PIXEL_HEIGHT / 2)
    DIVIDER_COLOUR = graphics.Color(0, 0, 255)

    for i in range(DIVIDER_POSITION[0], DIVIDER_POSITION[0] + config.PIXEL_WIDTH):
        canvas.SetPixel(i, DIVIDER_POSITION[1], DIVIDER_COLOUR.red, DIVIDER_COLOUR.green, DIVIDER_COLOUR.blue)

def draw_flight_details(canvas, font, font_small, parsed_data, FLIGHT_COUNTER, TEXT_COLOR_MAIN):
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
