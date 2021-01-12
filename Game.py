import pyglet
from pyglet import shapes
import math
import pygame
from helpermethods import linesCollided


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
    MAX_VELOCITY = 5
    MAX_ROTATION_VELOCITY = 5
    ACCELERATION = .1
    ROTATION_ACCELERATION = .3
    # FRICTION = .1
    FRICTION = .98

    def __init__(self, walls):
        self.x = Car.START_POS_X
        self.y = Car.START_POS_Y
        self.velx = 0
        self.vely = 0
        self.width = Car.WIDTH
        self.length = Car.LENGTH
        self.direction = vec2(0,1)
        self.acceleration = 0
        self.velocity = 0
        self.rotationAcceleration = 0
        self.rotationVelocity = 0
        self.driftMomentum = 0
        self.driftFriction = 0.87

        # self.dead = False

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

            #front line, left line, right line, back line
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
        # self.direction = ((self.carSprite.rotation + 90) % 360)

        self.updateControls()
        self.move()
        self.constraints()

    def constraints(self):
        #limit velocity
        if self.velocity > Car.MAX_VELOCITY:
            self.velocity = Car.MAX_VELOCITY
        elif self.velocity < -Car.MAX_VELOCITY:
            self.velocity = -Car.MAX_VELOCITY

        #limit turining velocity
        if self.rotationVelocity > Car.MAX_ROTATION_VELOCITY:
            self.rotationVelocity = Car.MAX_ROTATION_VELOCITY
        elif self.rotationVelocity < -Car.MAX_ROTATION_VELOCITY:
            self.rotationVelocity = -Car.MAX_ROTATION_VELOCITY


    def move(self):
        #forwards and backwards motion
        #friction
        # if not self.accelerating and not self.reversing:
        #     if self.velocity > .1:
        #         self.acceleration = -Car.FRICTION
        #     elif self.velocity < -.1:
        #         self.acceleration = Car.FRICTION
        #     else:
        #         self.velocity = 0
        #         self.acceleration=0






        # self.direction = ((self.carSprite.rotation + 90) % 360)

        # self.velocity += self.acceleration
        # self.velocity *= Car.FRICTION

        # x = math.cos(math.radians(self.direction))
        # y = math.sin(math.radians(self.direction))
        # driftVector = vec2(x, y)
        # # driftVector = driftVector.rotate(90)

        # addVector = vec2(0,0)
        # addVector.x += self.velocity * x
        # addVector.x += self.driftMomentum * driftVector.x
        # addVector.y += self.velocity * y
        # addVector.y += self.driftMomentum * driftVector.y
        # self.driftMomentum *= self.driftFriction

        # if addVector.length() != 0:
        #     addVector.normalize()

        # addVector.x * abs(self.velocity)
        # addVector.y * abs(self.velocity)

        # self.x += addVector.x
        # self.y += addVector.y





        # self.velocity += self.acceleration
        # self.velx = math.sin(self.direction * (math.pi / 180))
        # self.vely = math.cos(self.direction * (math.pi / 180))
        # self.x += self.velx * self.velocity
        # self.y += self.vely * self.velocity




        # #turning motion
        # self.rotationVelocity += self.rotationAcceleration

        # self.carSprite.rotation += self.rotationVelocity
        # self.carSprite.update(x=self.x, y=self.y)



        self.velocity += self.acc
        self.velocity *= Car.FRICTION
        # self.constrainVel()

        driftVector = vec2(self.direction)
        driftVector = driftVector.rotate(90)

        addVector = vec2(0, 0)
        addVector.x += self.velocity * self.direction.x
        addVector.x += self.driftMomentum * driftVector.x
        addVector.y += self.velocity * self.direction.y
        addVector.y += self.driftMomentum * driftVector.y
        self.driftMomentum *= self.driftFriction

        if addVector.length() != 0:
            addVector.normalize()

        addVector.x * abs(self.velocity)
        addVector.y * abs(self.velocity)

        self.x += addVector.x
        self.y += addVector.y




    def updateControls(self):
        # #forwards and backwards movement
        # if self.accelerating == True:
        #     self.acceleration = Car.ACCELERATION
        # elif self.reversing == True:
        #     self.acceleration = -Car.ACCELERATION
        # else:
        #     self.acceleration = 0

        # #turning movement 
        # if self.turningLeft and self.velocity > 0:
        #     self.rotationAcceleration = -Car.ROTATION_ACCELERATION
        # elif self.turningRight and self.velocity > 0:
        #     self.rotationAcceleration = Car.ROTATION_ACCELERATION

        # #turining is opposite when moving backwards
        # elif self.turningRight and self.velocity < 0:
        #     self.rotationAcceleration = -Car.ROTATION_ACCELERATION
        # elif self.turningLeft and self.velocity < 0:
        #     self.rotationAcceleration = Car.ROTATION_ACCELERATION
        # else:
        #     self.rotationAcceleration = 0
        #     self.rotationVelocity = 0


        # driftAmount = self.velocity * Car.MAX_ROTATION_VELOCITY
        # if self.velocity < 2:
        #     driftAmount = 0

        # if self.turningLeft:
        #     self.rotationVelocity -= Car.MAX_ROTATION_VELOCITY
        #     self.driftMomentum -= driftAmount
        # elif self.turningRight:
        #     self.rotationVelocity += Car.MAX_ROTATION_VELOCITY
        #     self.driftMomentum += driftAmount
        # else:
        #     self.rotationAcceleration = 0
        #     self.rotationVelocity = 0
        
        # if self.accelerating == True:
        #     self.acceleration = Car.ACCELERATION
        # elif self.reversing == True:
        #     self.acceleration = -Car.ACCELERATION
        # else:
        #     self.acceleration = 0

        multiplier = 1
        if abs(self.velocity) < 5:
            multiplier = abs(self.velocity) / 5
        if self.velocity < 0:
            multiplier *= -1

        driftAmount = self.velocity * Car.MAX_ROTATION_VELOCITY * self.width / (9.0 * 8.0)
        if self.velocity < 5:
            driftAmount = 0

        if self.turningLeft:
            self.direction = self.direction.rotate(math.degrees(Car.MAX_ROTATION_VELOCITY) * multiplier)

            self.driftMomentum -= driftAmount
        elif self.turningRight:
            self.direction = self.direction.rotate(-math.degrees(Car.MAX_ROTATION_VELOCITY) * multiplier)
            self.driftMomentum += driftAmount
        self.acc = 0
        if self.accelerating:
            if self.velocity < 0:
                self.acceleration = 3 * Car.ACCELERATION
            else:
                self.acc = Car.ACCELERATION
        elif self.reversing:
            if self.velocity > 0:
                self.acceleration = -3 * Car.ACCELERATION
            else:
                self.acceleration = -1 * Car.ACCELERATION




    def render(self):
        # self.hitWall()
        self.update()
        self.carSprite.draw()
