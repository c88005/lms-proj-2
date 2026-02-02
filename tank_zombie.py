import arcade
from zombie import Zombie

class TankZombie(Zombie):
    def __init__(self):
        super().__init__()
        self.color = arcade.color.AVOCADO
        self.dead_color = arcade.color.ARMY_GREEN
        self.base_speed = 120
        self.speed_multiplier = 1
        self.sz = 75
        self.attack_dmg = 5
        self.health = 55
        self.attack_cd = 1.5
        self.type = "tank_zombie"

