import pyglet
import math


class GameObject:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0
        self.direction = 0
        self.rotateVel = 200
        self.keys = dict(left=False, right=False, up=False, down=False)

        image = pyglet.image.load("car.png")

        self.sprite = pyglet.sprite.Sprite(image, x=self.posx, y=self.posy)
        self.sprite.scale = .05
        self.sprite.rotation = -90
        self.sprite.image.anchor_x = self.sprite.image.width / 2
        self.sprite.image.anchor_y = self.sprite.image.height / 2

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.sprite.x += self.velx*dt
        self.sprite.y += self.vely*dt
        if self.keys['left']:
            self.rotateVel = 200
            self.sprite.rotation -= self.rotateVel * dt
        if self.keys['right']:
            self.rotateVel = 200
            self.sprite.rotation += self.rotateVel * dt
        if self.keys['up']:
            self.move(1)
        if self.keys['down']:
            self.move(-1)

    def move(self, forwards):
        direction = ((self.sprite.rotation + 90) % 360)
        self.velx = forwards * math.sin(direction * (math.pi / 180)) * 300
        self.vely = forwards * math.cos(direction * (math.pi / 180)) * 300






