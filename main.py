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

    # initialize the brain common to every instance
    brain = model.Brain(2*game.height*game.width, 3);

    trainer = instance.Training(brain, 0.95)
#    trainer.agent.load();

    # training agent
    for i in range(epochs):
        trainer.reset_epoch();
        for j in range(ticks):
            if(j % 1000 == 0):
                average_reward = trainer.get_average();
                total_games = trainer.num_games;
                print('Epoch {}'.format(i+1)+' progress {}%'.format(j/100.0)+ ' Average collected score is {}'.format(average_reward)+' across {} games.'.format(total_games));

            trainer.advance(j);

        # save at the end of epoch
        print('End of Epoch...');
        trainer.agent.save()

    
elif mode == 2:
    import app
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '700')
    tetrisGame = game.Game();

    brain = model.Brain(2*game.height*game.width, 3);
    tetrisAgent = agent_a2c.A2C(brain, 0.95);
    tetrisAgent.load();
    app.TetrisApp(tetrisGame, tetrisAgent).run();    










