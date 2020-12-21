from Game import Game
import pyglet

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game()
    def on_draw(self):
        self.game.render()





        
if __name__ == "__main__":
    window = GameWindow(1800, 1000, "AI racing game")
    pyglet.app.run()