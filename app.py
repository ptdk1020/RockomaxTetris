import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import game

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')

tetrisGame = game.Game();

class TetrisWidget(Widget):
    def __init__(self, **kwargs):
        super(TetrisWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self.press, self)
        self._keyboard.bind(on_key_down=self.press)
    
    def update(self, *args):
        self.canvas.clear();
        with self.canvas:
            for i in range(0,10):
                for j in range(0,20):
                    # Add a blue color
                        if(tetrisGame.boardandpiece[0,j,i] == 1):
                            Color(0, 1.0, 0)
                            # Add a square for the inactive Tetris piece blocks
                            Rectangle(pos=(200+30*i, 50+30*j), size=(30, 30))
            for i in range(0,10):
                for j in range(0,20):
                    # Add a red color
                        if(tetrisGame.boardandpiece[1,j,i] == 1):
                            Color(1., 0, 0)
                            # Add a square for the active Tetris piece blocks
                            Rectangle(pos=(200+30*i, 50+30*j), size=(30, 30))
                            

    def press(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            tetrisGame.left();
        if keycode[1] == 'right':
            tetrisGame.right();
        if keycode[1] == 'up':
            tetrisGame.up();
        if keycode[1] == 'down':
            tetrisGame.down();
        if keycode[1] == 'spacebar':
            print("spacebar");
        self.update();
        return True

class TetrisApp(App):
    def build(self):
        tetrisapp = TetrisWidget()
        Clock.schedule_interval(tetrisapp.update, 0.5)
        Clock.schedule_interval(tetrisGame.update,0.5)
        return tetrisapp

if __name__ == "__main__":
    TetrisApp().run()