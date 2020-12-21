import pyglet

class Game:
    def __init__(self):
        trackImg = pyglet.image.load('images/track.png')
        self.trackSprite = pyglet.sprite.Sprite(trackImg, x=0, y=0)

        self.car = Car()

    def render(self):
        self.trackSprite.draw()
        self.car.redraw()

class Car:
    START_POS_X = 250
    START_POS_Y = 250
    WIDTH = 40
    HEIGHT = 20

    def __init__(self):
        self.x = Car.START_POS_X
        self.y = Car.START_POS_Y
        self.width = Car.WIDTH
        self.height = Car.HEIGHT

        self.dead = False

        self.carPic = pyglet.image.load("images/car.png")
        self.carSprite = pyglet.sprite.Sprite(self.carPic, x = self.x, y=self.y)
        self.carSprite.update(rotation=0, scale_x=self.width / self.carSprite.width, scale_y=self.height / self.carSprite.height)


    def redraw(self):
        self.carSprite.draw()
