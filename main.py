import game
import model
import agent_a2c
import instance
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

<<<<<<< Updated upstream
    # initialize and load DQL agent
    tetrisAgent = agent.DQL(400, 4, 0.95)
    tetrisAgent.load()
=======
    # initialize the brain common to every instance
    brain = model.Brain(2*game.height*game.width, 3);
>>>>>>> Stashed changes

    trainer = instance.Training(brain, 0.95)
    trainer.agent.load();

    # training agent
    for i in range(epochs):
<<<<<<< Updated upstream
        # initialize number of games and total score
        num_games = 0
        total_score = 0
        for j in range(ticks):
            if(j % 500 == 0):
                print('Epoch progress {}%'.format(j/100.0))
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
            tetrisGame.update_visibleboard();
            # update agent
            tetrisAgent.update(tetrisGame.getReward(), tetrisGame.boardandpiece.flatten())
=======
        trainer.reset_epoch();
        for j in range(ticks):
            if(j % 1000 == 0):
                average_reward = trainer.get_average();
                print('Epoch {}'.format(i+1)+' progress {}%'.format(j/100.0)+ ' Average collected score is {}.'.format(average_reward));

            trainer.advance(j);
>>>>>>> Stashed changes

        # save at the end of epoch
        print('End of Epoch...');
        trainer.agent.save()

    
elif mode == 2:
    import app
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '700')
    tetrisGame = game.Game();
<<<<<<< Updated upstream
    tetrisAgent = agent.DQL(400,4, 0.95);
=======
    brain = model.Brain(2*game.height*game.width, 3);
    tetrisAgent = agent_a2c.A2C(brain, 0.95);
>>>>>>> Stashed changes
    tetrisAgent.load();
    app.TetrisApp(tetrisGame, tetrisAgent).run();    










