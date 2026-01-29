import arcade
import math
from particles import Particle
import random


#basically this is a way simpler entity than sprite entity, and i dont know if id have enough time to make sprite ones
class Entity:
    def __init__(self,x=0,y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.sz = 50
        self.color = arcade.color.WHITE
        self.dead_color = arcade.color.LIGHT_GRAY

        self.base_speed = 1
        self.speed_multiplier = 1
        self.active_ai = True
        self.moves = False
        self.attack_dmg = 1
        self.health = 10
        self.attack_cd = 0.5
        self.can_attack = True
        self.attack_wait = 0
        self.is_dead = False
        self.type = "entity"
        self.initmsg = "entity module is initialized"

        print(self.initmsg)

    def draw(self, world):
        coords = world.get_world_coords()
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x + coords[0], self.y + coords[1],
                                                 self.sz, self.sz),
                                self.color)

    def create_hurt_particles(self, particle_array, world):
        for i in range(random.randint(5,15)):
            p = Particle(x=self.x, y=self.y)
            p_array = p.setup_new_particle(p)
            particle_array.append(p)
            if p.lifetime <= 0:
                particle_array.remove(p_array)

    def get_position(self):
        return self.x, self.y

    def hurt(self, sound_sys, particle_array, dtype, damage, damage_sys, world, dt):
        if self.health > 0:
            if self.health - damage <= 0:
                self.health = 0
                self.die()
            n = float(random.randint(800, 1100)) / 1000
            sound_sys.play_sound(damage_sys.sound_from_damage(dtype), 0.25, n)
            self.create_hurt_particles(particle_array, world)
            self.health -= damage

    def die(self):
        self.is_dead = True
        self.active_ai = False
        self.color = self.dead_color

    def get_world_position(self, world):
        coords = world.get_world_coords()
        return self.x + coords[0], self.y + coords[1]

    def get_angle_to(self, dx, dy, world):
        coords = self.get_world_position(world)
        return math.atan2(coords[1] - dy, coords[0] - dx)

    def set_position(self,x,y):
        self.x = x
        self.y = y
        return self.x, self.y

    def recreate_entity(self, x, y, entity_type, health, dmg, speed, active):
        self.x = x
        self.y = y
        self.type = entity_type
        self.health = health
        self.attack_dmg = dmg
        self.base_speed = speed
        self.active_ai = active

    def get_health(self):
        return self.health

    def set_health(self,health):
        self.health = health

    def get_damage(self):
        return self.attack_dmg

    def set_damage(self,damage):
        self.attack_dmg = damage

    def get_speed(self):
        return self.base_speed

    def set_speed(self,speed):
        self.base_speed = speed

    def get_type(self):
        return self.type