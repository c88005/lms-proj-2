class World:
    def __init__(self):
        self.x = 0
        self.y = 0

        print("world system is initialized")

    def set_world_coords(self, x, y):
        self.x = x
        self.y = y

    def set_world_x(self, x):
        self.x = x

    def add_world_x(self, x):
        self.x += x

    def set_world_y(self, y):
        self.y = y

    def add_world_y(self, y):
        self.y += y

    def get_world_coords(self):
        return self.x, self.y
