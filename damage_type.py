class Damage:
    def __init__(self, sys):
        self.sounds = {
            "bullet" : sys.get_sound("flesh"),
            "kill": sys.get_sound("crit"),
            "blade": sys.get_sound("slash"),
            "all": sys.get_sound("gore"),
            "blunt": sys.get_sound("heavy"),
            "light_blunt": sys.get_sound("stun")
        }

        self.initmsg = "damage module is initialized"

    def sound_from_damage(self, dtype):
        return self.sounds[dtype]