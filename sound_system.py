from sys import exception

import arcade
import random


class SoundSystem:
    def __init__(self):
        bolt = self.create_sound("assets/sounds/bolt.mp3")
        pump = self.create_sound("assets/sounds/pump.mp3")
        rifle = self.create_sound("assets/sounds/rifle.mp3")
        equip_pistol = self.create_sound("assets/sounds/equip_pistol.ogg")
        equip = self.create_sound("assets/sounds/equip.ogg")
        equip_rifle = self.create_sound("assets/sounds/rifle_equip.mp3")
        pistol2 = self.create_sound("assets/sounds/pistol_fire.mp3")
        pistol = self.create_sound("assets/sounds/lpistol.mp3")
        shotgun = self.create_sound("assets/sounds/shotgun_fire.ogg")
        slash = self.create_sound("assets/sounds/slash.mp3")
        stun = self.create_sound("assets/sounds/stun.mp3")
        gore = self.create_sound("assets/sounds/gore.mp3")
        kill = self.create_sound("assets/sounds/mw2.mp3")
        hit_flesh = self.create_sound("assets/sounds/hit_flesh.mp3")
        hit_bludgeon = self.create_sound("assets/sounds/blunt_kill.mp3")
        walk = self.create_sound_variance([
            "assets/sounds/walk1.mp3",
            "assets/sounds/walk2.mp3",
            "assets/sounds/walk3.mp3",
            "assets/sounds/walk4.mp3"
        ])
        headshot = self.create_sound_variance([
            "assets/sounds/headshot1.mp3",
            "assets/sounds/headshot2.mp3"
        ])

        self.sound_list = {
            # reload and shi
            "bolt": bolt,
            "pump": pump,
            # misc
            "kill": kill,
            # fire
            "fire_rifle": rifle,
            "fire_pistol": pistol,
            "fire_pistol2": pistol2,
            "fire_shotgun": shotgun,
            # equips
            "eq_pistol": equip_pistol,
            "eq": equip,
            "eq_rifle": equip_rifle,
            #
            "walk": walk,
            # damage sounds
            "crit": headshot,
            "slash": slash,
            "flesh": hit_flesh,
            "heavy": hit_bludgeon,
            "gore": gore,
            "stun": stun,
        }


        print("sound system is initialized")


    def get_sound(self, name):
        return self.sound_list[name]

    def create_sound(self, location):
        return arcade.load_sound(f"{location}")

    def create_sound_variance(self, locations):
        variance = []
        for location in locations:
            variance.append(self.create_sound(location))

        return variance

    def play_variance(self, variance, volume=1, pitch=1):
        if isinstance(variance, list):
            rnd = random.randint(0, len(variance) - 1)
            arcade.play_sound(variance[rnd], volume, 0, False, pitch)
            return variance[rnd]
        else:
            print("Sound provided is NOT a variance")
            return "dummas"

    def play_sound(self, sound, volume=1, pitch=1):
        if not isinstance(sound, list):
            arcade.play_sound(sound, volume, 0, False, pitch)
            return sound
        else:
            print("Sound provided is NOT a sound (its a variance)")
            return "dummas"