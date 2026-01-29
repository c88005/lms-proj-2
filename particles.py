import arcade
import math
import random


class Particle:
    def __init__(self,x=0,y=0,sz=20,color=arcade.color.DESIRE,min_spread=-20,max_spread=20,min_dist=-1,max_dist=1,lifetime=3):
        super().__init__()
        self.x = x
        self.y = y
        self.sz = sz
        self.color = color
        self.minspr = min_spread
        self.maxspr = max_spread
        self.mindist = min_dist
        self.maxdist = max_dist
        self.lifetime = lifetime

    def draw(self, world):
        coords = world.get_world_coords()
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x + coords[0], self.y + coords[1],
                                                 self.sz, self.sz),
                                self.color)

    def get_position(self):
        return self.x, self.y

    def get_world_position(self, world):
        coords = world.get_world_coords()
        return self.x + coords[0], self.y + coords[1]

    def set_position(self,x,y):
        self.x = x
        self.y = y
        return self.x, self.y

    def setup_new_particle(self, particle):
        spreadx = random.randint(self.minspr, self.maxspr)
        spready = random.randint(self.minspr, self.maxspr)
        dist = random.randint(self.mindist, self.maxdist) // 100

        return particle, spreadx, spready, dist

    def action(self, dt, spreadx, spready, dist):
        self.lifetime -= 1 * dt
        if dist > (spreadx + spready):
            dist -= (spreadx + spready)
            spready -= spready * dt * 90
            spreadx -= spreadx * dt * 90
            self.x += spreadx * dt * 2
            self.y += spready * dt * 2
        if self.lifetime <= 0:
            if self.sz > 0:
                self.sz -= 1 * dt * 20


class Line:
    def __init__(self,x=0,y=0,dx=0,dy=0,sz=4,color=arcade.color.YELLOW,lifetime=0,can_damage=True,damage=5):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.sz = sz
        self.color = color
        self.can_damage = can_damage
        self.lifetime = lifetime
        self.damage = damage

    def draw(self, world):
        coords = world.get_world_coords()
        arcade.draw_line(
            self.x, self.y,
            self.dx, self.dy,
            self.color,self.sz
        )

    def action(self, dt, array):
        self.lifetime -= 1 * dt
        if self.lifetime <= 0:
            if self.sz > 0:
                self.sz -= dt * 40
            else:
                for ray in array:
                    if self in ray:
                        array.remove(ray)
