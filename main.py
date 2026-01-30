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
        self.workbench = None
        self.scrapper = None
        self.background_color = arcade.color.BLACK
        self.time_t = 0
        self.keys = []
        self.mouse_buttons = []
        self.mouse_x = 0
        self.mouse_y = 0

        self.wave_counter = 0
        self.intermission = True
        self.intermission_timer = 3

        self.menu = False
        self.wave_song = None

        self.ray_array = []
        self.grass_array = []
        self.particle_array = []
        self.useless_gui_sprite_array = arcade.SpriteList()
        self.shop_gui = arcade.SpriteList()
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
        self.workbench = Object(100, 450, "assets/textures/workbench.png", 75)
        self.scrapper = Object(170, 450, "assets/textures/scrapper.png", 75)
        self.rifle_buy_button = Object(240, 420, "assets/textures/button.png", 1)
        self.shop_gui.append(self.rifle_buy_button)
        self.useless_gui_sprite_array.append(health_bg)
        for _ in range(self.calc.rnd(35, 60)):
            c = self.world.get_world_coords()
            self.grass_array.append(Object(self.calc.rnd(-800, 800), self.calc.rnd(-800, 800),
                                           "assets/textures/grass.png", 55))
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
            if self.menu:
                pass
            else:
                self.game_draw()

    def shop_draw(self):
        self.gui.create_rect(self.player.x, self.player.y, 500, 500, (0, 0, 0, 150))
        self.shop_gui.draw(pixelated=True)

    def game_draw(self):
        self.background_color = arcade.color.RUSSIAN_GREEN
        # self.ent.draw(self.world)
        for grass in self.grass_array:
            grass.draw_as_rect(self.world)
        self.workbench.draw_as_rect(self.world)
        self.scrapper.draw_as_rect(self.world)
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
            wave_text = self.gui.create_text(f"ИНТЕРМИССИЯ", 405, 470, arcade.color.WHITE, 30, 160)
            wave_textint = self.gui.create_text(str(self.intermission_timer)[0:4], 370, 430, arcade.color.WHITE, 30, 160)
        else:
            wave_text = self.gui.create_text(f"ВОЛНА: {self.wave_counter}", 405, 470, arcade.color.WHITE, 30, 160)
        #self.shop_draw()

    def wave_start(self):
        #self.sound_sys.play_sound(self.sound_sys.get_sound("wave"), 0.35)
        self.intermission = False
        self.wave_counter += 1
        self.wave_song = self.sound_sys.play_variance(self.sound_sys.get_sound("wave_song"), 0.25, loop=True)
        for _ in range(5 * self.wave_counter):
            a = Zombie()
            a.x = 0 + self.calc.rnd(-800, 800)
            a.y = 0 + self.calc.rnd(-800, 800)
            a.base_speed += self.calc.rnd(-50, 10)
            self.mob_array.append(a)

    def wave_end(self):
        #self.sound_sys.play_sound(self.sound_sys.get_sound("wave"), 0.35)
        self.intermission = True
        self.wave_song[0].stop(self.wave_song[1])
        self.mob_array.clear()
        self.intermission_timer = 30

    def game_update(self, delta_time):
        c = self.world.get_world_coords()
        # print(self.mouse_buttons)
        if self.intermission:
            if self.intermission_timer > 0:
                self.intermission_timer -= 1 * delta_time
            else:
                self.intermission_timer = 0
                self.wave_start()
        else:
            if self.mob_array == []:
                self.wave_end()
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

            #OVERLAYS ARE BROKEN
            if self.player.overlay:
                self.player.draw_screen_overlay(delta_time, (255, 0, 0, 125), 1)
            for mob in self.mob_array:
                mob.ai(self.player, self.world, delta_time, self.particle_array,
                       self.sound_sys, self.damage_sys, self.calc)
                if mob.is_dead:
                    if mob.dead_time < 3:
                        mob.dead_time += 1 * delta_time
                    else:
                        self.mob_array.remove(mob)
                for ray in self.ray_array:
                    if ray[0].can_damage:
                        mob_c = mob.get_world_position(self.world)

                        if self.calc.rudimentary_raycast((ray[0].x,ray[0].y), (ray[0].dx, ray[0].dy),
                                                         (mob_c[0], mob_c[1]), 50) and not mob.is_dead :
                            mob.hurt(self.sound_sys, self.particle_array, "bullet",
                                     ray[0].damage, self.damage_sys, self.world, delta_time)
                            if mob.is_dead:
                                self.player.kills += 1
                                n = float(self.calc.rnd(800, 1200)) / 1000
                                self.sound_sys.play_sound(self.sound_sys.get_sound("kill"), 0.25)
                                self.sound_sys.play_sound(self.sound_sys.get_sound("gore"), 0.35, n)
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
            if self.menu:
                pass
            else:
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