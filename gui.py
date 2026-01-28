import arcade


class Gui:
    def __init__(self):
        pass

    def create_rect(self, x, y, sx, sy, color):
        rect = arcade.draw_rect_filled(arcade.rect.XYWH(x, y,sx, sy),color)
        return rect


