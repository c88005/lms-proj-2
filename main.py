import arcade
from sound_system import SoundSystem
from calculate import Calc
from world import World
from entity import Entity
from zombie import Zombie
from player import Player
from damage_type import Damage
from gui import Gui
from object import Object


class Engine(arcade.Window):
    def __init__(self):

        super().__init__(810, 540, "Engine", antialiasing=True)
        self.initialized = False
        print("engine thread is initialized")
        self.sound_sys = None
        self.player = None
        self.world = None
        self.damage_sys = None
        self.gui = None
        self.calc = None
        self.background_color = arcade.color.BLACK
        self.time_t = 0
        self.keys = []
        self.mouse_buttons = []
        self.mouse_x = 0
        self.mouse_y = 0

        self.wave_counter = 0
        self.intermission = True

        self.menu = False

        self.ray_array = []
        self.particle_array = []
        self.useless_gui_sprite_array = arcade.SpriteList()
        self.mob_array = []

        self.ent = Entity()

    def setup(self):
        self.sound_sys = SoundSystem()
        self.calc = Calc()
        self.damage_sys = Damage(self.sound_sys)
        self.gui = Gui()
        self.player = Player()
        self.world = World()
        health_bg = Object(125, 35, "assets/textures/health_bg.png")
        self.useless_gui_sprite_array.append(health_bg)
        for _ in range(5):
            a = Zombie()
            a.x = 500 + self.calc.rnd(-50, 50)
            a.y = 270 + self.calc.rnd(-50, 50)
            a.base_speed = 150 + self.calc.rnd(-50, 50)
            self.mob_array.append(a)
        self.initialized = True

    def on_draw(self):
        self.clear()
        if not self.initialized:

            self.background_color = arcade.color.BLACK
            #arcade.draw_text()
            arcade.draw_text("Initializing...", 405, 300, arcade.color.WHITE,
                             70, 150, "center", "Arial", anchor_x="center" )
            arcade.draw_text("please wait a little bit", 405, 50, arcade.color.WHITE,
                             15, 150, "center", "Arial", anchor_x="center")
            self.setup()
        else:
            self.game_draw()


    def game_draw(self):
        self.background_color = arcade.color.RUSSIAN_GREEN
        # self.ent.draw(self.world)
        for particle in self.particle_array:
            #print(self.particle_array) DONT TURN THIS ON GAME LAGS SO BADLY
            particle[0].draw(self.world)
        for ray in self.ray_array:
            ray[0].draw(self.world)
        for mob in self.mob_array:
            mob.draw(self.world)
        self.player.draw()
        self.useless_gui_sprite_array.draw()
        health_text = self.gui.create_text(f"HP:{self.player.get_health()}", 80, 20, arcade.color.WHITE, 24, 160)
        if self.intermission:
            wave_text = self.gui.create_text(f"INTERMISSION", 405, 470, arcade.color.WHITE, 30, 160)
        else:
            wave_text = self.gui.create_text(f"WAVE: {self.wave_counter}", 405, 470, arcade.color.WHITE, 30, 160)
        self.player_c = self.player.get_position()
        self.mouse_c = self.get_true_position_of(self.world, self.mouse_x, self.mouse_y)
        arcade.draw_line(
            self.player_c[0], self.player_c[1],
            self.mouse_x, self.mouse_y,
            arcade.color.WHITE, 5
        )

    def game_update(self, delta_time):
        c = self.world.get_world_coords()
        # print(self.mouse_buttons)
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
            ray[0].action(delta_time, self.ray_array)
        if self.player != None:
            self.player.move(self.keys, self.sound_sys, delta_time, self.calc, self.world)
            self.player.mouse_actions(self.mouse_buttons, self.sound_sys, delta_time, self.calc, self.world,
                                      self.ray_array, [self.mouse_x, self.mouse_y])

            if self.player.overlay:
                self.player.draw_screen_overlay(delta_time, (255, 0, 0, 125), 1)
            for mob in self.mob_array:
                mob.ai(self.player, self.world, delta_time, self.particle_array,
                       self.sound_sys, self.damage_sys, self.calc)
                for ray in self.ray_array:
                    if ray[0].can_damage:
                        player_c = self.player.get_position()
                        mouse_c = [self.mouse_x, self.mouse_y]
                        mob_c = mob.get_world_position(self.world)

                        if self.calc.rudimentary_raycast((player_c[0],player_c[0]), (mouse_c[0], mouse_c[1]),
                                                         (mob_c[0], mob_c[1]), 50):
                            mob.hurt(self.sound_sys, self.particle_array, "bullet",
                                     ray[0].damage, self.damage_sys, self.world, delta_time)
                            ray[0].can_damage = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.player.weapon_rotation_update(x, y, self.calc)
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button not in self.mouse_buttons:
            if button == 4:
                self.player.weapon = 2
            self.mouse_buttons.append((button, x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        for b in self.mouse_buttons:
            if button in b:
                self.mouse_buttons.remove(b)
                if button == 1: self.player.reset_fire()

    def on_update(self, delta_time):
        if self.initialized:
            self.game_update(delta_time)

    def on_key_press(self, key, modifiers):
        if key not in self.keys:
            self.keys.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys:
            self.keys.remove(key)

    def get_true_position_of(self, world, x, y):
        coords = world.get_world_coords()
        return -(coords[0] - x), -(coords[1] - y)


def main():
    thread = Engine()
    arcade.run()

if __name__ == "__main__":
    main()