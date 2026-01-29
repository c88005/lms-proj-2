import arcade
from sound_system import SoundSystem
from calculate import Calc
from world import World
from entity import Entity
from zombie import Zombie
from player import Player
from damage_type import Damage


class Engine(arcade.Window):
    def __init__(self):

        super().__init__(810, 540, "Engine", antialiasing=True)
        self.initialized = False
        print("engine thread is initialized")
        self.sound_sys = None
        self.player = None
        self.world = None
        self.calc = None
        self.background_color = arcade.color.BLACK
        self.time_t = 0
        self.keys = []
        self.mouse_buttons = []
        self.mouse_x = 0
        self.mouse_y = 0

        self.ray_array = []
        self.particle_array = []
        self.mob_array = []

        self.ent = Entity()
        self.zombie = Zombie()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        if not self.initialized:

            self.background_color = arcade.color.BLACK
            #arcade.draw_text()
            arcade.draw_text("Initializing...", 405, 300, arcade.color.WHITE,
                             70, 150, "center", "Arial", anchor_x="center" )
            arcade.draw_text("please wait a little bit", 405, 50, arcade.color.WHITE,
                             15, 150, "center", "Arial", anchor_x="center")
            self.sound_sys = SoundSystem()
            self.calc = Calc()
            self.damage_sys = Damage(self.sound_sys)
            self.player = Player()
            self.world = World()
            self.initialized = True
        else:
            self.background_color = arcade.color.RUSSIAN_GREEN
            #self.ent.draw(self.world)
            for particle in self.particle_array:
                particle[0].draw(self.world)
            for ray in self.ray_array:
                ray.draw(self.world)
            self.zombie.draw(self.world)
            self.player.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.weapon_rotation_update(x, y, self.calc)
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button not in self.mouse_buttons:
            self.mouse_buttons.append((button, x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        for b in self.mouse_buttons:
            if button in b:
                self.mouse_buttons.remove(b)
                if button == 1: self.player.reset_fire()

    def on_update(self, delta_time):
        if self.initialized:
            c = self.world.get_world_coords()
            #print(self.mouse_buttons)
            for particle in self.particle_array:
                if particle[0].sz <= 0:
                    self.particle_array.remove(particle)
                particle[0].action(
                    delta_time,
                    particle[1],
                    particle[2],
                    particle[3]
                )
            for ray in self.ray_array:
                print(self.ray_array)
                ray.action(delta_time, self.ray_array)
            if self.player != None:
                self.player.move(self.keys, self.sound_sys, delta_time, self.calc, self.world)
                self.player.mouse_actions(self.mouse_buttons, self.sound_sys, delta_time, self.calc, self.world, self.ray_array)
                if self.player.overlay:
                    self.player.draw_screen_overlay(delta_time, (255, 0, 0, 125), 1)
                self.zombie.ai(self.player, self.world, delta_time, self.particle_array,
                               self.sound_sys, self.damage_sys, self.calc)

    def on_key_press(self, key, modifiers):
        if key not in self.keys:
            self.keys.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys:
            self.keys.remove(key)


def main():
    thread = Engine()
    thread.setup()
    arcade.run()

if __name__ == "__main__":
    main()