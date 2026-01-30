import arcade
from entity import Entity
import math
from object import Object
import random
from particles import *


class Player(Entity):
    def __init__(self):
        super().__init__(405, 270)
        self.x = 405
        self.y = 270
        self.new_x = 0
        self.new_y = 0
        self.base_speed = 150
        self.active_ai = False
        self.attack_dmg = 1
        self.health = 10
        self.type = "player"
        #no multiplayer yet
        self.third_party = False
        self.client = True
        self.name = ""
        self.weapon = 1
        self.can_shoot = True
        self.weapon_cd = 0
        self.light_ammo = 48
        self.medium_ammo = 32
        self.long_ammo = 90
        self.heavy_ammo = 32

        self.additional = arcade.SpriteList()
        self.weapon_img = Object(self.x, self.y - 10, sz=2.5)

        self.additional.append(self.weapon_img)

        self.step_sound_cd = 1

        self.overlay = False
        self.overlay_time = 0
        self.overlay_alpha = 125

        self.currency = 100
        self.kills = 0

        self.initmsg = "player is initialized"

        print(self.initmsg)

    def weapon_rotation_update(self, x, y, calc):
        if self.weapon == 1:
            weapon_texture = "assets/textures/pistol.png"
        elif self.weapon == 2:
            weapon_texture = "assets/textures/pistol2.png"
        elif self.weapon == 3:
            weapon_texture = "assets/textures/ak74.png"
        else:
            weapon_texture = "assets/textures/placeholder.png"

        if self.weapon_img.angle >= 135 or self.weapon_img.angle <= -45:
            self.weapon_img.change_texture(weapon_texture, True, True)
        else:
            self.weapon_img.change_texture(weapon_texture, False, True)

        angle = calc.look_at(self.x, self.y, x, y)
        if not self.is_dead:
            self.weapon_img.angle = math.degrees(-angle) + 45

    def draw(self):
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y, self.sz, self.sz),
                                self.color)
        self.additional.draw(pixelated=True)

    def move(self, keys, sound_sys, dt, calc, world):
        self.step_sound_cd -= 2.75 * dt
        if self.client:
            if not self.is_dead:
                for key in keys:
                    if key == arcade.key.A:
                        self.moves = True
                        if self.step_sound_cd <= 0:
                            self.step_sound_cd = 1
                            sound_sys.play_variance(sound_sys.get_sound("walk"), 0.25)
                        world.add_world_x(self.base_speed * dt)
                        self.new_x += (self.base_speed * dt)
                    elif key == arcade.key.D:
                        self.moves = True
                        if self.step_sound_cd <= 0:
                            self.step_sound_cd = 1
                            sound_sys.play_variance(sound_sys.get_sound("walk"), 0.25)
                        world.add_world_x(-(self.base_speed * dt))
                        self.new_x += -(self.base_speed * dt)
                    elif key == arcade.key.W:
                        self.moves = True
                        if self.step_sound_cd <= 0:
                            self.step_sound_cd = 1
                            sound_sys.play_variance(sound_sys.get_sound("walk"), 0.25)
                        world.add_world_y(-(self.base_speed * dt))
                        self.new_y += -(self.base_speed * dt)
                    elif key == arcade.key.S:
                        self.moves = True
                        if self.step_sound_cd <= 0:
                            self.step_sound_cd = 1
                            sound_sys.play_variance(sound_sys.get_sound("walk"), 0.25)
                        world.add_world_y(self.base_speed * dt)
                        self.new_y += (self.base_speed * dt)
                    else:
                        self.moves = False

    def mouse_actions(self, buttons, sound_sys, dt, calc, world, ray_array, mouse):
        if self.client:
            if not self.is_dead:
                if self.weapon_cd > 0:
                    self.weapon_cd -= 1 * dt
                for button in buttons:
                    if button[0] == 1:
                        if self.weapon_cd <= 0:
                            self.shoot(sound_sys, dt, calc, world, ray_array, button, mouse)

    def shoot(self, sound_sys, dt, calc, world, ray_array, button, mouse):
        if self.weapon == 1:
            r = Line(x=self.x, y=self.y, dx=mouse[0], dy=mouse[1], damage=3, can_damage=True)
            ray_array.append([r, r.can_damage, r.damage])
            sound_sys.play_sound(sound_sys.get_sound("fire_pistol"))
            self.weapon_cd = 0.2
        elif self.weapon == 2:
            if not self.can_shoot: return
            self.can_shoot = False
            r = Line(x=self.x, y=self.y, dx=button[1], dy=button[2], damage=5, can_damage=True)
            ray_array.append([r, r.can_damage, r.damage])
            sound_sys.play_sound(sound_sys.get_sound("fire_pistol2"))
            self.weapon_cd = 0.25

    def reset_fire(self):
        self.can_shoot = True

    def get_true_position(self, world):
        coords = world.get_world_coords()
        return -(coords[0] - self.x), -(coords[1] - self.y)

    def create_hurt_particles(self, particle_array, world):
        coords = self.get_true_position(world)
        for i in range(random.randint(5,15)):
            p = Particle(x=coords[0], y=coords[1])
            p_array = p.setup_new_particle(p)
            particle_array.append(p_array)
            if p.lifetime <= 0:
                particle_array.remove(p_array)

    def hurt(self, sound_sys, particle_array, dtype, damage, damage_sys, world, dt):
        if self.health > 0:
            if self.health - damage <= 0:
                self.health = 0
                self.die()
            self.overlay = True
            self.overlay_alpha = 125
            self.overlay_time = 0
            n = float(random.randint(800, 1100)) / 1000
            sound_sys.play_sound(damage_sys.sound_from_damage(dtype), 0.25, n)
            self.create_hurt_particles(particle_array, world)
            self.health -= damage

    def draw_screen_overlay(self, dt, color, time):
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y,810, 540),color)
        color = (color[0], color[1], color[2], self.overlay_alpha)
        if self.overlay_time > 0:
            self.overlay_alpha -= dt * time
            self.overlay_time -= dt
        else:
            self.overlay = False

    def get_angle_to(self, dx, dy):
        return math.atan2(self.y - dy, self.x - dx)