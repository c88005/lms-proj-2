import arcade
import random
from entity import Entity
import math

class Zombie(Entity):
    def __init__(self):
        super().__init__(500, 270)
        self.color = arcade.color.AMAZON
        self.base_speed = 140
        self.speed_multiplier = 1
        self.active_ai = True
        self.moves = False
        self.attack_dmg = 1
        self.health = 15
        self.attack_cd = 0.75
        self.type = "zombie"
        self.initmsg = "zombie module is initialized"

        print(self.initmsg)

    def ai(self, player, world, dt, particle_array, sound_sys, damage_sys, calc):
        if self.active_ai:
            player_coords = player.get_true_position(world)
            coords = self.get_world_position(world)
            if not calc.collision(player_coords, self.get_position(), 50, 50, -1, 0):

                angle = player.get_angle_to(coords[0], coords[1], world)
                x = math.cos(angle) * self.base_speed,
                y = math.sin(angle) * self.base_speed,
                self.y += (y[0]) * dt
                self.x += (x[0]) * dt
                self.angle = math.degrees(-angle)
                self.moves = True
            else:
                self.moves = False
                if self.can_attack:
                    self.can_attack = False
                    self.attack_wait = 0
                    self.attack(1, player, particle_array, sound_sys, damage_sys, world, dt)

                else:
                    if self.attack_wait < self.attack_cd:
                        self.attack_wait += dt / self.attack_cd
                    else:
                        self.can_attack = True



    def attack(self, damage, ent, particle_array, sound_sys, damage_sys, world, dt):
        ent.hurt(sound_sys, particle_array, "light_blunt", damage, damage_sys, world, dt)