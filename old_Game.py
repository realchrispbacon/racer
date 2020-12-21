
import pyglet

START_POS_X = 258
START_POS_Y = 288

class Game:
    def __init__(self):
        pass

class Car:
    START_POS_X = 258
    START_POS_Y = 288

    def __init__(self):
        self.x = START_POS_X
        self.y = START_POS_Y
        self.dead = False

        self.carPic = pyglet.image.load('images/car.png')

    def update(self):
        if not self.dead:
            self.move()
    def move(self):
        pass
