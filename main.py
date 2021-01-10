from Game import Game
import pyglet
from pyglet.window import key

frameRate = 30.0

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game()
        self.car = self.game.car

    def on_draw(self):
        self.car.render()
        self.game.render()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.car.turningRight = True

        if symbol == key.LEFT:
            self.car.turningLeft = True

        if symbol == key.UP:
            self.car.accelerating = True

        if symbol == key.DOWN:
            self.car.reversing = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.car.turningRight = False

        if symbol == key.LEFT:
            self.car.turningLeft = False

        if symbol == key.UP:
            self.car.accelerating = False
            
        if symbol == key.DOWN:
            self.car.reversing = False

    def update(self, dt):
        self.car.update()


if __name__ == "__main__":
    window = GameWindow(1800, 1000, "AI racing game")
    pyglet.clock.schedule_interval(window.update, 1/frameRate)
    pyglet.app.run()