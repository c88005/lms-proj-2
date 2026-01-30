import random
import arcade
import math
import sound_system


class Calc:
    def __init__(self):
        print("calculation module is initialized")

    def collision(self, pos1, pos2, sz1, sz2, direction, speed):
        # (directions: 0 - X, 1 - Y, 2 - -X, 3 - -Y, -1 - NONE, -2 - LINE COLLISION)
        # (i wanted to deprecate this direction thing, but what arcade has to offer js sucks)

        # I FINALLY REALIZED HOW TO MAKE IT, BUT THIS SYSTEM IS HORRIBLE

        # AND PLAYER HAS SOME SPACE LEFT AFTER COLLISION IS DONE
        if direction == 0:
            if ((pos1[0] + sz1 // 2 + speed * 2 >= pos2[0] - sz2 // 2) and (
                    pos1[0] - sz1 // 2 - speed * 1 < pos2[0] + sz2 // 2)
                    and (pos1[1] + sz1 // 2 + speed * 1 >= pos2[1] - sz2 // 2) and (
                            pos1[1] - sz1 // 2 - speed * 1 < pos2[1] + sz2 // 2)):
                pos1[1] -= speed * 5
                return True
            else:
                return False

        elif direction == 1:
            if ((pos1[0] + sz1 // 2 + speed * 1 >= pos2[0] - sz2 // 2) and (
                    pos1[0] - sz1 // 2 - speed * 1 < pos2[0] + sz2 // 2)
                    and (pos1[1] + sz1 // 2 + speed * 2 >= pos2[1] - sz2 // 2) and (
                            pos1[1] - sz1 // 2 - speed * 2 < pos2[1] + sz2 // 2)):
                pos1[1] -= speed * 5
                return True
            else:
                return False

        elif direction == 2:
            if -((pos1[0] + sz1 // 2 + speed * 1 >= pos2[0] - sz2 // 2) and -(
                    pos1[0] - sz1 // 2 - speed * 2 < pos2[0] + sz2 // 2)
                    and -(pos1[1] + sz1 // 2 + speed * 1 >= pos2[1] - sz2 // 2) and -(
                            pos1[1] - sz1 // 2 - speed * 1 < pos2[1] + sz2 // 2)):
                pos1[1] -= speed * 5
                return True
            else:
                return False


        elif direction == 3:
            if -((pos1[0] + sz1 // 2 + speed * 1 >= pos2[0] - sz2 // 2) and -(
                    pos1[0] - sz1 // 2 - speed * 2 < pos2[0] + sz2 // 2)
                 and -(pos1[1] + sz1 // 3 + speed * 3 >= pos2[1] - sz2 // 2) and -(
                            pos1[1] - sz1 // 2 - speed * 3 < pos2[1] + sz2 // 2)):
                pos1[1] -= speed * 5
                return True
            else:
                return False
        elif direction == -1:
            if ((pos1[0] + sz1 // 2 >= pos2[0] - sz2 // 2) and (
                    pos1[0] - sz1 // 2 < pos2[0] + sz2 // 2)
                    and (pos1[1] + sz1 // 2 >= pos2[1] - sz2 // 2) and (
                            pos1[1] - sz1 // 2 < pos2[1] + sz2 // 2)):
                return True
            else:
                return False
        elif direction == -2:
            if (pos1[0] - sz1 // 2 <= pos2[0][0] <= pos1[0] + sz1 // 2 and
                pos1[1] - sz1 // 2 <= pos2[0][1] <= pos1[1] + sz1 // 2) or \
                    (pos1[0] - sz1 // 2 <= pos2[1][0] <= pos1[0] + sz1 // 2 and
                     pos1[1] - sz1 // 2 <= pos2[1][1] <= pos1[1] + sz1 // 2):
                return True
            else:
                return False
        else:
            return False

    def rnd(self, a, b):
        return random.randint(a, b)

    def look_at(self, x, y, dx, dy):
        angle = math.atan2(dy - y, dx - x)
        return angle

    def rudimentary_raycast(self, point1, point2, pos, sz, step=30):
        a = self.look_at(point1[0], point1[1], point2[0], point2[1])
        b = math.cos(a) * step,
        c = math.sin(a) * step,
        d = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) / step
        for i in range(math.floor(d)):
            np = (point1[0] + b[0] * i, point1[1] + c[0] * i)
            if self.collision(pos, np, sz, 5, -1, 0):
                return True

        return False
