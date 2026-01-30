import arcade
import math
import os.path


class Object(arcade.Sprite):
    def __init__(self,x=0,y=0,texture="assets/textures/placeholder.png",sz=1):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.sz = sz
        if not os.path.isfile(texture) or texture.strip() == "":
            self.texture = arcade.load_texture("assets/textures/placeholder.png")
            self.scale = self.sz
        else:
            self.texture = arcade.load_texture(texture)
            self.scale = self.sz
        self.type = "object"
        self.initmsg = "object module is initialized"

        #print(self.initmsg)

    def draw_as_rect(self, world):
        c = world.get_world_coords()
        return arcade.draw_texture_rect(self.texture,
                                         arcade.rect.XYWH(self.center_x + c[0], self.center_y + c[1],
                                                          self.sz, self.sz), pixelated=True)

    def change_texture(self, texture, flip=False, gun=False):
        if not os.path.isfile(texture) or texture.strip() == "":
            self.texture = arcade.load_texture("assets/textures/placeholder.png")
        else:
            if flip:
                if gun:
                    self.texture = arcade.load_texture(texture).flip_diagonally().rotate_180()
                else:
                    self.texture = arcade.load_texture(texture).flip_diagonally()
            else:
                self.texture = arcade.load_texture(texture)

    def get_position(self):
        return self.center_x, self.center_y

    def get_world_position(self, world):
        coords = world.get_world_coords()
        return self.center_x + coords[0], self.center_y + coords[1]

    def get_angle_to(self, dx, dy, world):
        coords = self.get_world_position(world)
        return math.atan2(coords[1] - dy, coords[0] - dx)

    def set_position(self,x,y):
        self.center_x = x
        self.center_y = y
        return self.center_x, self.center_y

    def get_type(self):
        return self.type