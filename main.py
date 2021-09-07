import game
from kivy.config import Config

# choosing a mode
mode = -1
while mode not in range(3):
    print("Choose a mode:\n 0. Manual plays \n 1. AI loop plays \n 2. Watch mode")
    mode = int(input())

if mode == 0:
    import app
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '700')
    tetrisGame = game.Game()
    app.TetrisApp(tetrisGame).run()
elif mode == 1:
    epochs = 1000











