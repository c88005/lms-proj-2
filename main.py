import math
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
        self.scrap_multiplier = 1

        self.wave_counter = 0
        self.intermission = True
        self.intermission_timer = 10

        self.menu = False
        self.wave_song = None
        self.shop_weapon_cost = 450
        self.can_click_shop = True

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
        scrap = Object(650, 35, "assets/textures/scrap_icon.png", 2.5)
        ammo = Object(650, 75, "assets/textures/ammo.png", 2.5)
        self.workbench = Object(100, 450, "assets/textures/workbench.png", 75)
        self.scrapper = Object(170, 450, "assets/textures/scrapper.png", 75)
        bandage_buy_button = Object(240, 420, "assets/textures/button.png", 1)
        wpn_upgrade_button = Object(240, 330, "assets/textures/button.png", 1)
        ammo_buy_button = Object(240, 240, "assets/textures/button.png", 1)
        self.shop_gui.append(wpn_upgrade_button)
        self.shop_gui.append(bandage_buy_button)
        self.shop_gui.append(ammo_buy_button)
        self.useless_gui_sprite_array.append(scrap)
        self.useless_gui_sprite_array.append(ammo)
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

    def upgrade_weapon(self):
        if self.player.scrap_parts >= self.shop_weapon_cost and self.player.weapon != 3:
            self.sound_sys.play_sound(self.sound_sys.get_sound("scrap"),0.5)
            self.sound_sys.play_sound(self.sound_sys.get_sound("bolt"), 0.25)
            self.player.weapon += 1
            self.player.scrap_parts -= self.shop_weapon_cost
            if self.player.weapon != 3:
                self.shop_weapon_cost *= 2
            else:
                self.shop_weapon_cost = "Распродано"
        else:
            self.sound_sys.play_sound(self.sound_sys.get_sound("marker"), 0.25, 1.5)

    def heal_player(self):
        if self.player.scrap_parts >= 20:
            self.sound_sys.play_sound(self.sound_sys.get_sound("scrap"),0.45)
            self.sound_sys.play_sound(self.sound_sys.get_sound("stim"), 0.55)
            self.player.health += 2
            self.player.scrap_parts -= 20
        else:
            self.sound_sys.play_sound(self.sound_sys.get_sound("marker"), 0.25, 1.5)

    def craft_ammo(self):
        if self.player.scrap_parts >= 5:
            self.sound_sys.play_sound(self.sound_sys.get_sound("scrap"),0.45)
            self.sound_sys.play_sound(self.sound_sys.get_sound("eq_rifle"), 0.55)
            self.player.light_ammo += 30
            self.player.medium_ammo += 30
            self.player.long_ammo += 30
            self.player.scrap_parts -= 5
        else:
            self.sound_sys.play_sound(self.sound_sys.get_sound("marker"), 0.25, 1.5)

    def shop_draw(self):
        self.gui.create_rect(self.player.x, self.player.y, 500, 500, (0, 0, 0, 150))
        self.shop_gui.draw(pixelated=True)
        bandage_price = self.gui.create_text(f"20 SP", 200, 410, arcade.color.WHITE, 24, 160)
        weapon_price = self.gui.create_text(f"{self.shop_weapon_cost} SP", 200, 320, arcade.color.WHITE, 24, 160)
        ammo_price = self.gui.create_text(f"5 SP", 200, 230, arcade.color.WHITE, 24, 160)
        bandage_name = self.gui.create_text(f"Сделать бинт", 450, 410, arcade.color.WHITE, 24, 160, align="left")
        upgrade_pistol = self.gui.create_text(f"Обновить оружие", 470, 320, arcade.color.WHITE, 24, 160, align="left")
        craft_bullets = self.gui.create_text(f"Сделать патроны", 475, 230, arcade.color.WHITE, 24, 160, align="left")
        shop_name = self.gui.create_text("Верстак", 400, 60, arcade.color.WHITE, 30, 160)

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

        self.useless_gui_sprite_array.draw(pixelated=True)
        health_text = self.gui.create_text(f"HP:{self.player.get_health()}", 80, 20, arcade.color.WHITE, 24, 160)
        scrap_text = self.gui.create_text(f"SP:{self.player.scrap_parts}", 700, 20, arcade.color.WHITE, 24, 160)
        if self.player.weapon == 1: cur_ammo = self.player.light_ammo
        elif self.player.weapon == 2: cur_ammo = self.player.medium_ammo
        elif self.player.weapon == 3: cur_ammo = self.player.long_ammo
        ammo_text = self.gui.create_text(f"AM:{cur_ammo}", 700, 60, arcade.color.WHITE, 24, 160)
        if self.intermission:
            wave_text = self.gui.create_text(f"ИНТЕРМИССИЯ", 405, 470, arcade.color.WHITE, 30, 160)
            wave_textint = self.gui.create_text(str(self.intermission_timer)[0:4], 370, 430, arcade.color.WHITE, 30, 160)
        else:
            wave_text = self.gui.create_text(f"ВОЛНА: {self.wave_counter}", 405, 470, arcade.color.WHITE, 30, 160)
        if self.player.in_shop:
            self.shop_draw()

    def wave_start(self):
        self.intermission = False
        self.wave_counter += 1
        if self.wave_counter % 5 == 0:
            self.scrap_multiplier *= 2.5
            self.sound_sys.play_sound(self.sound_sys.get_sound("wave"), 0.35)
            self.wave_song = self.sound_sys.play_sound(self.sound_sys.get_sound("boss_wave"), 0.25, loop=True)
        else:
            self.scrap_multiplier *= 1.25
            self.wave_song = self.sound_sys.play_variance(self.sound_sys.get_sound("wave_song"), 0.25, loop=True)

        for _ in range(5 * self.wave_counter):
            a = Zombie()
            a.x = 0 + self.calc.rnd(-800, 800)
            a.y = 0 + self.calc.rnd(-800, 800)
            if self.wave_counter % 5 == 0:
                a.base_speed += self.calc.rnd(-40, 30)
            else:
                a.base_speed += self.calc.rnd(-50, 10)
            self.mob_array.append(a)

    def wave_end(self):
        #self.sound_sys.play_sound(self.sound_sys.get_sound("wave"), 0.35)
        self.intermission = True
        self.wave_song[0].stop(self.wave_song[1])
        self.wave_song = self.sound_sys.play_sound(self.sound_sys.get_sound("storm"), 0.05, loop=True)
        self.mob_array.clear()
        self.intermission_timer = 15

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
            if self.calc.collision(self.player.get_position(), self.workbench.get_world_position(self.world), 50, 50, -1, 0):
                self.player.in_shop = True
            else:
                self.player.in_shop = False
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
                                self.player.scrap_parts += math.floor(self.calc.rnd(1, 15) * self.scrap_multiplier)
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
            self.mouse_buttons.append((button, x, y))
            print(x, y)
            if self.player.in_shop:
                if not self.can_click_shop: return
                if button == 4 and x > 164 and x < 315 and y > 397 and x < 447:
                    self.can_click_shop = False
                    self.heal_player()
                elif button == 4 and x > 164 and x < 315 and y > 303 and x < 356:
                    self.can_click_shop = False
                    self.upgrade_weapon()
                elif button == 4 and x > 164 and x < 315 and y > 212 and x < 268:
                    self.can_click_shop = False
                    self.craft_ammo()

    def on_mouse_release(self, x, y, button, modifiers):
        for b in self.mouse_buttons:
            if button in b:
                self.mouse_buttons.remove(b)
                if button == 1: self.player.reset_fire()
            if button in b and button == 4:
                self.can_click_shop = True

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