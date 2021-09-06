from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config


Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '700')


class TetrisGame(Widget):
    pass


class TetrisApp(App):
    def build(self):
        return TetrisGame()


if __name__ == '__main__':
    TetrisApp().run()