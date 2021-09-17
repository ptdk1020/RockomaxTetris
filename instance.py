import agent_a2c
import game

class Training():
    
    def __init__(self, main_model, gamma):
        self.agent = agent_a2c.A2C(main_model, gamma);
        self.game = game.Game();
        self.reset_epoch();
        self.game_length = 0;
        
    def get_average(self):
        if(self.num_games != 0):
            return self.total_score/self.num_games;
        else:
            return 0;
        
    def reset_epoch(self):
        self.total_score = 0;
        self.num_games = 0;
        
    def advance(self, tick):
        
        if tick % 1 == 0: #updating the game every x tick
            self.game.update()
            self.game_length +=1;
        
        # possible game end processing
        if self.game.game_over == True or self.game_length > 2000:
                self.agent.update(0);
                self.agent.learn(self.game.boardandpiece.flatten());
                self.game_length = 1;
                self.num_games += 1
                self.total_score += self.game.getScore()
                self.game.start()
                self.game.update()

        self.game.check_lines();

        if self.game_length != 1: #Collecting rewards except on the first game tick
            self.agent.update(self.game.getReward())
        if self.game_length % 5 == 0: # Teaching the agent every 5 ticks from game start
            self.agent.learn(self.game.boardandpiece.flatten());
        action = self.agent.select_action(self.game.boardandpiece.flatten())

        if action == 0:
            self.game.left();
        if action == 1:
            self.game.right();
        if action == 2:
            self.game.down();
        if action == 3:
            self.game.up();
        self.game.update_visibleboard();