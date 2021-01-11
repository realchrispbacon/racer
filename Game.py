import pyglet
from pyglet import shapes
import math
import pygame
from helpermethods import *


vec2 = pygame.math.Vector2

class Game:
    def __init__(self):
        trackImg = pyglet.image.load('images/track.png')
        self.trackSprite = pyglet.sprite.Sprite(trackImg, x=0, y=0)

        self.walls = []
        self.setWalls()

        self.car = Car(self.walls)

    def setWalls(self):
        #outside
        self.walls.append(Wall(974,29,350,40))
        self.walls.append(Wall(350,40,297,71))
        self.walls.append(Wall(297,71,269,105))
        self.walls.append(Wall(269,105,210,359))
        self.walls.append(Wall(210,359,200,413))
        self.walls.append(Wall(200,413,218,601))
        self.walls.append(Wall(218,601,306,748))
        self.walls.append(Wall(306,748,553,828))
        self.walls.append(Wall(553,828,873,819))
        self.walls.append(Wall(873,819,1177,787))
        self.walls.append(Wall(1177,787,1223,736))
        self.walls.append(Wall(1223,736,1223,640))
        self.walls.append(Wall(1223,640,1170,577))
        self.walls.append(Wall(1170,577,1050,539))
        self.walls.append(Wall(1050,539,765,400))
        self.walls.append(Wall(765,400,1103,433))
        self.walls.append(Wall(1103,433,1259,538))
        self.walls.append(Wall(1259,538,1350,572))
        self.walls.append(Wall(1350,572,1458,583))
        self.walls.append(Wall(1458,583,1555,554))
        self.walls.append(Wall(1555,554,1622,515))
        self.walls.append(Wall(1622,515,1725,326))
        self.walls.append(Wall(1725,326,1692,124))
        self.walls.append(Wall(1692,124,1617,80))
        self.walls.append(Wall(1617,80,1520,34))
        self.walls.append(Wall(1520,34,974,29))

        #inside
        self.walls.append(Wall(1498,110,1007,111))
        self.walls.append(Wall(1007,111,411,120))
        self.walls.append(Wall(411,120,360,143))
        self.walls.append(Wall(360,143,331,179))
        self.walls.append(Wall(331,179,283,388))
        self.walls.append(Wall(283,388,282,571))
        self.walls.append(Wall(282,571,328,646))
        self.walls.append(Wall(328,646,368,686))
        self.walls.append(Wall(368,686,570,763))
        self.walls.append(Wall(570,763,1106,717))
        self.walls.append(Wall(1106,717,1118,677))
        self.walls.append(Wall(1118,677,1043,618))
        self.walls.append(Wall(1043,618,680,450))
        self.walls.append(Wall(680,450,616,395))
        self.walls.append(Wall(616,395,605,332))
        self.walls.append(Wall(605,332,634,297))
        self.walls.append(Wall(634,297,716,288))
        self.walls.append(Wall(716,288,1133,360))
        self.walls.append(Wall(1133,360,1315,485))
        self.walls.append(Wall(1315,485,1446,503))
        self.walls.append(Wall(1446,503,1525,488))
        self.walls.append(Wall(1525,488,1578,464))
        self.walls.append(Wall(1578,464,1658,301))
        self.walls.append(Wall(1658,301,1632,182))
        self.walls.append(Wall(1632,182,1498,110))

    def render(self):

        self.trackSprite.draw()
        
        for w in self.walls:
            w.draw()
            
        self.car.render()

class Wall():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.line = shapes.Line(self.x1, self.y1, self.x2, self.y2, width=2)

    def draw(self):
        self.line.draw()

    def turnRed(self):
        red = (255,0,0)
        self.line.color = red
    def turnWhite(self):
        white = (255,255,255)
        self.line.color = white


class Car:
    START_POS_X = 250
    START_POS_Y = 250
    LENGTH = 40
    WIDTH = 20
    TOP_SPEED = 2
    ROTATION_VELOCITY = 2

    def __init__(self, walls):
        self.x = Car.START_POS_X
        self.y = Car.START_POS_Y
        self.velx = 0
        self.vely = 0
        self.width = Car.WIDTH
        self.length = Car.LENGTH
        self.direction = 0

        self.dead = False

        #pyglet defs
        self.carPic = pyglet.image.load("images/car.png")
        self.carSprite = pyglet.sprite.Sprite(self.carPic, x = self.x, y=self.y)
        self.carSprite.update(rotation=-90, scale_x=self.length / self.carSprite.width, scale_y=self.width / self.carSprite.height)
        #to center the rotation around the center of the car
        self.carSprite.image.anchor_x = self.carSprite.image.width / 2
        self.carSprite.image.anchor_y = self.carSprite.image.height / 2

        #moving booleans
        self.turningRight = False
        self.turningLeft = False
        self.accelerating = False
        self.reversing = False

        self.walls = walls

    def hitWall(self):
        self.direction = -self.direction

        FRcornerX = self.x + Car.WIDTH/2 * math.cos(math.radians(self.direction)) - Car.LENGTH/2 * math.sin(math.radians(self.direction))
        FRcornerY = self.y + Car.WIDTH/2 * math.sin(math.radians(self.direction)) + Car.LENGTH/2 * math.cos(math.radians(self.direction))

        FLcornerX = self.x - Car.WIDTH/2 * math.cos(math.radians(self.direction)) - Car.LENGTH/2 * math.sin(math.radians(self.direction))
        FLcornerY = self.y - Car.WIDTH/2 * math.sin(math.radians(self.direction)) + Car.LENGTH/2 * math.cos(math.radians(self.direction))

        BLcornerX = self.x - Car.WIDTH/2 * math.cos(math.radians(self.direction)) + Car.LENGTH/2 * math.sin(math.radians(self.direction))
        BLcornerY = self.y - Car.WIDTH/2 * math.sin(math.radians(self.direction)) - Car.LENGTH/2 * math.cos(math.radians(self.direction))

        BRcornerX = self.x + Car.WIDTH/2 * math.cos(math.radians(self.direction)) + Car.LENGTH/2 * math.sin(math.radians(self.direction))
        BRcornerY = self.y + Car.WIDTH/2 * math.sin(math.radians(self.direction)) - Car.LENGTH/2 * math.cos(math.radians(self.direction))

        # FRcircle = shapes.Circle(FRcornerX, FRcornerY, 5, color=(255,0,0))
        # FLcircle = shapes.Circle(FLcornerX, FLcornerY, 5, color=(255,0,0))
        # BRcircle = shapes.Circle(BRcornerX, BRcornerY, 5, color=(255,0,0))
        # BLcircle = shapes.Circle(BLcornerX, BLcornerY, 5, color=(255,0,0))

        # FRcircle.draw()
        # FLcircle.draw()
        # BRcircle.draw()
        # BLcircle.draw()

        for wall in self.walls:
            #front line
            if linesCollided(wall.x1, wall.y1, wall.x2, wall.y2, FLcornerX, FLcornerY, FRcornerX, FRcornerY) or \
                linesCollided(wall.x1, wall.y1, wall.x2, wall.y2, FLcornerX, FLcornerY, BLcornerX, BLcornerY) or \
                linesCollided(wall.x1, wall.y1, wall.x2, wall.y2, FRcornerX, FRcornerY, BRcornerX, BRcornerY) or \
                linesCollided(wall.x1, wall.y1, wall.x2, wall.y2, BLcornerX, BLcornerY, BRcornerX, BRcornerY):
                wall.turnRed()
                # return True
            else:
                wall.turnWhite()
                # return False
            


    def update(self):
        self.direction = ((self.carSprite.rotation + 90) % 360)

        if self.accelerating == True:
            self.velx = math.sin(self.direction * (math.pi / 180))
            self.vely = math.cos(self.direction * (math.pi / 180))
            self.x = self.x + self.velx * Car.TOP_SPEED
            self.y = self.y + self.vely * Car.TOP_SPEED

        if self.reversing == True:
            self.velx = math.sin(self.direction * (math.pi / 180))
            self.vely = math.cos(self.direction * (math.pi / 180))
            self.x = self.x - self.velx * Car.TOP_SPEED
            self.y = self.y - self.vely * Car.TOP_SPEED

        if self.accelerating:
            if self.turningLeft == True:
                self.carSprite.rotation -= Car.ROTATION_VELOCITY
            if self.turningRight == True:
                self.carSprite.rotation += Car.ROTATION_VELOCITY
        if self.reversing:
            if self.turningLeft == True:
                self.carSprite.rotation += Car.ROTATION_VELOCITY
            if self.turningRight == True:
                self.carSprite.rotation -= Car.ROTATION_VELOCITY

        self.carSprite.update(x=self.x, y=self.y)


    def render(self):

        self.hitWall()

        self.update()
        self.carSprite.draw()
