import pyglet
from pyglet.window import key
from GameObject import GameObject


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/30.0

        self.car = GameObject(200, 200)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.car.keys['right'] = True
        if symbol == key.LEFT:
            self.car.keys['left'] = True
        if symbol == key.UP:
            self.car.keys['up'] = True
        if symbol == key.DOWN:
            self.car.keys['down'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.car.keys['right'] = False
        if symbol == key.LEFT:
            self.car.keys['left'] = False
        if symbol == key.UP:
            self.car.keys['up'] = False
        if symbol == key.DOWN:
            self.car.keys['down'] = False
        self.car.velx = 0
        self.car.vely = 0

    def on_draw(self):
        self.clear()
        self.car.draw()

    def update(self, dt):
        self.car.update(dt)


if __name__ == "__main__":
    window = MyWindow(800, 600, "Driver", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
