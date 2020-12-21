
# from Game import Game
import pyglet

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.set_minimum_size(400, 300)
		# set background color
		pyglet.gl.glClearColor(0.5,0,0,1) # Note that these are values 0.0 - 1.0 and not (0-255).

		#backgroundColor = [0, 0, 0, 255]
		#backgroundColor = [i / 255 for i in backgroundColor]
		# load background image
		# self.game = Game()
		# self.ai = QLearning(self.game)

	def update(self):
		pass

if __name__ == "__main__":
	window = GameWindow(300, 300, "AI racing game", resizable=False)
	#pyglet.clock.schedule_interval(window.update, 1 / frameRate)
	pyglet.app.run()
