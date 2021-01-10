import pyglet
import math

class Game:
    def __init__(self):
        trackImg = pyglet.image.load('images/track.png')
        self.trackSprite = pyglet.sprite.Sprite(trackImg, x=0, y=0)

        self.car = Car()

    def render(self):
        self.trackSprite.draw()
        self.car.render()

class Car:
    START_POS_X = 250
    START_POS_Y = 250
    WIDTH = 40
    HEIGHT = 20
    TOP_SPEED = 2
    ROTATION_VELOCITY = 2

    def __init__(self):
        self.x = Car.START_POS_X
        self.y = Car.START_POS_Y
        self.velx = 0
        self.vely = 0
        self.width = Car.WIDTH
        self.height = Car.HEIGHT
        self.direction = 0

        self.dead = False

        #pyglet defs
        self.carPic = pyglet.image.load("images/car.png")
        self.carSprite = pyglet.sprite.Sprite(self.carPic, x = self.x, y=self.y)
        self.carSprite.update(rotation=0, scale_x=self.width / self.carSprite.width, scale_y=self.height / self.carSprite.height)
        #to center the rotation around the center of the car
        self.carSprite.image.anchor_x = self.carSprite.image.width / 2
        self.carSprite.image.anchor_y = self.carSprite.image.height / 2

        #moving booleans
        self.turningRight = False
        self.turningLeft = False
        self.accelerating = False
        self.reversing = False


    def update(self):
        direction = ((self.carSprite.rotation + 90) % 360)

        if self.accelerating == True:
            self.velx = math.sin(direction * (math.pi / 180))
            self.vely = math.cos(direction * (math.pi / 180))
            self.x = self.x + self.velx * Car.TOP_SPEED
            self.y = self.y + self.vely * Car.TOP_SPEED

        if self.reversing == True:
            self.velx = math.sin(direction * (math.pi / 180))
            self.vely = math.cos(direction * (math.pi / 180))
            self.x = self.x + self.velx * Car.TOP_SPEED
            self.y = self.y + self.vely * Car.TOP_SPEED

        if self.turningLeft == True:
            self.carSprite.rotation -= Car.ROTATION_VELOCITY

        if self.turningRight == True:
            self.carSprite.rotation += Car.ROTATION_VELOCITY

        self.carSprite.update(x=self.x, y=self.y)


    def render(self):
        self.update()
        self.carSprite.draw()
