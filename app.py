from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.graphics import Color, Rectangle

import game

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')

tetrisGame = game.Game();

class Time(Widget):
    def update(self, *args):
        self.canvas.clear();
        with self.canvas:
            for i in range(0,10):
                for j in range(0,20):
                    # Add a red color
                        if(tetrisGame.boardandpiece[0,j,i] == 1):
                            Color(0, 1.0, 0)
                            # Add a square for the active Tetris piece blocks
                            Rectangle(pos=(200+30*i, 50+30*j), size=(30, 30))
            for i in range(0,10):
                for j in range(0,20):
                    # Add a red color
                        if(tetrisGame.boardandpiece[1,j,i] == 1):
                            Color(1., 0, 0)
                            # Add a square for the active Tetris piece blocks
                            Rectangle(pos=(200+30*i, 50+30*j), size=(30, 30))

class TetrisApp(App):
    def build(self):
        tetrisapp = Time()
        Clock.schedule_interval(tetrisapp.update, 1)
        Clock.schedule_interval(tetrisGame.update,1)
        return tetrisapp

if __name__ == "__main__":
    TetrisApp().run()