import game
import model
import agent_a2c
import instance
import my_optim
from kivy.config import Config

num_agents = 10;

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
    epochs = 100
    ticks = 10000

    #Initialize the brain and optimizer common to every trainer
    brain = model.Brain(2*game.height*game.width, 3);
    brain.share_memory();
    optimizer = my_optim.SharedAdam(brain.parameters(), 0.0005)
    optimizer.share_memory()

    trainers = []; #Each trainer runs its own instance of Tetris
    for k in range(num_agents):
        new_trainer = instance.Training(brain,optimizer,0.95);
        trainers.append(new_trainer);

    #trainers[0].agent.load();

    # training agent
    for i in range(epochs):
        for x in trainers:    
            x.reset_epoch();
        for j in range(ticks):
            if((j+1) % 1000 == 0):
                average_reward = 0;
                total_games = 0;
                for x in trainers:
                    average_reward += x.get_average()/num_agents;
                    total_games += x.num_games;
                print('Epoch {}'.format(i+1)+' progress {}%'.format((j+1)/100.0)+ ' Average collected score is {}'.format(average_reward)+' across {} games.'.format(total_games));

            for x in trainers:
                x.advance(j);

        # save at the end of epoch
        print('End of Epoch...');
        trainers[0].agent.save()

    
elif mode == 2:
    import app
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '700')
    tetrisGame = game.Game();

    brain = model.Brain(2*game.height*game.width, 3);
    optimizer = my_optim.SharedAdam(brain.parameters(), 0.001)
    tetrisAgent = agent_a2c.A2C(brain, optimizer, 0.95);
    tetrisAgent.load();
    app.TetrisApp(tetrisGame, tetrisAgent).run();    










