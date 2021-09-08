import game
import agent
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
    epochs = 10
    ticks = 10000
    avg_scores = 0

    # initialize and load DQL agent
    tetrisAgent = agent.DQL(400, 4, 0.99)
    #tetrisAgent.load()

    # initialize number of games and total score
    num_games = 0
    total_score = 0

    #initialize a game
    tetrisGame = game.Game()
    tetrisGame.update()

    # training agent
    for i in range(epochs):
        for j in range(ticks):
            if (j+1) % 5 == 0:
                tetrisGame.update()


            # possible game end processing
            if tetrisGame.game_over == True:
                num_games += 1
                total_score += tetrisGame.getScore()
                print('Epoch {} :'.format(i+1)+' Average score after {} games is {}'.format(num_games, total_score/num_games))
                tetrisGame.start()
                tetrisGame.update()

            # action selection
            action = tetrisAgent.select_action(tetrisGame.boardandpiece.flatten())
            if action == 0:
                tetrisGame.left()
            if action == 1:
                tetrisGame.up()
            if action == 2:
                tetrisGame.right()
            if action == 3:
                tetrisGame.down()

            # update agent
            tetrisAgent.update(tetrisGame.getReward(), tetrisGame.boardandpiece.flatten())

        # save at the end of epoch
        print('End of Epoch...');
        tetrisAgent.save()

    
elif mode == 2:
    import app
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '700')
    tetrisGame = game.Game();
    tetrisAgent = agent.DQL(400,4, 0.99);
    tetrisAgent.load();
    app.TetrisApp(tetrisGame, tetrisAgent).run();    










