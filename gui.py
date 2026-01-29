import arcade


class Gui:
    def __init__(self):
        print("gui is initialized")

    def create_rect(self, x, y, sx, sy, color):
        rect = arcade.draw_rect_filled(arcade.rect.XYWH(x, y,sx, sy),color)
        return rect

    def create_text(self, text, x, y, color, size, width, align="center"):
        text = arcade.draw_text(text, x, y, color,
                         size, width, align, "Arial", anchor_x="center")
        return text