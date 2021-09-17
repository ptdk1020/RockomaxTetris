import numpy as np
import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

import game


class TetrisWidget(Widget):
    def __init__(self, tetrisGame, agent = 0, **kwargs):
        super(TetrisWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self.press, self)
        self._keyboard.bind(on_key_down=self.press)
        self.tetrisGame = tetrisGame
        self.agent = agent;
        self.tick = 0;
    
    def update(self, *args):
        if(self.tick % 5 == 0): #Game updates once every 5 ticks
            self.tetrisGame.update();
        self.draw();
        if(self.agent != 0):
            self.playAgent();
        self.tick += 1;
        
    def draw(self):
        self.canvas.clear();
        with self.canvas:
            for i in range(0,game.width):
                for j in range(0,game.height):
                    # Add a blue color
                        if(self.tetrisGame.boardandpiece[0,j,i] == 1):
                            Color(0, 1.0, 0)
                            # Add a square for the inactive Tetris piece blocks
                            Rectangle(pos=(200+30*i, 50+30*j), size=(30, 30))
            for i in range(0,game.width):
                for j in range(0,game.height):
                    # Add a red color
                        if(self.tetrisGame.boardandpiece[1,j,i] == 1):
                            Color(1., 0, 0)
                            # Add a square for the active Tetris piece blocks
                            Rectangle(pos=(200+30*i, 50+30*j), size=(30, 30))      

    def press(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.tetrisGame.left();
        if keycode[1] == 'right':
            self.tetrisGame.right();
        if keycode[1] == 'up':
            self.tetrisGame.up();
        if keycode[1] == 'down':
            self.tetrisGame.down();
        if keycode[1] == 'spacebar':
            print("spacebar");
        if keycode[1] == 'r':
            self.tetrisGame.start();
        self.tetrisGame.update_visibleboard();
        self.draw();
        return True
    
    def playAgent(self, *args):
        action = self.agent.select_action(self.tetrisGame.boardandpiece.flatten(), True)
        if(action == 0):
            self.tetrisGame.left();
        if(action == 1):
            self.tetrisGame.up();
        if(action == 2):
            self.tetrisGame.right();
        if(action == 3):
            self.tetrisGame.down();
        self.tetrisGame.update_visibleboard();

class TetrisApp(App):
    def __init__(self, tetrisGame, agent = 0):
        App.__init__(self)
        self.tetrisGame = tetrisGame
        self.agent = agent;

    def build(self):
        tetrisapp = TetrisWidget(self.tetrisGame, self.agent)
        Clock.schedule_interval(tetrisapp.update, 0.1)
        return tetrisapp

# if __name__ == "__main__":
#     TetrisApp().run()