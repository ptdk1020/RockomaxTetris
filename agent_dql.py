# Importing the libraries

import numpy as np
import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable

#Brain

class Brain(nn.Module):
    
    def __init__(self, input_size, nb_actions):
        super(Brain, self).__init__();
        self.input_size = input_size;
        self.nb_action = nb_actions;
        self.fc1 = nn.Linear(input_size, 2000);
        self.fc2 = nn.Linear(2000, 500);
        self.fc3 = nn.Linear(500, nb_actions);
        
    def forward(self, state):
        x = F.relu(self.fc1(state));
        x = F.relu(self.fc2(x));
        #x = F.relu(self.fc3(x));
        #x = F.relu(self.fc4(x));
        #x = F.relu(self.fc5(x));
        #x = F.relu(self.fc6(x));
        q_values = self.fc3(x)
        return q_values;
    
#Experience replay

class ReplayMemory():
    
    def __init__(self, capacity):
        self.capacity = capacity;
        self.memory = [];
        
    def push(self, event):
        self.memory.append(event);
        if len(self.memory) > self.capacity:
            del self.memory[0];
        
    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size));
        return map(lambda x: Variable(torch.cat(x, 0)), samples);
        
#Deep Q-Learning

class DQL():
    def __init__(self, input_size, nb_actions, gamma):
        self.gamma = gamma;
        self.model = Brain(input_size, nb_actions);
        self.memory = ReplayMemory(250); #Memory capacity of 250
        self.optimizer = optim.Adam(self.model.parameters(), lr = 0.001); #Learning rate 0.005
        self.last_state = torch.Tensor(input_size).unsqueeze(0).float();
        self.last_action = 0;
        self.last_reward = 0;
        
    def select_action(self,state, training = True):
        if(training):
            probs = F.softmax(self.model(Variable(torch.from_numpy(state).unsqueeze(0).float()))*1); # T=1
            readableqs = self.model(Variable(torch.from_numpy(state).unsqueeze(0).float())).detach().numpy();
            readableprobs = probs.detach().numpy();
            action = probs.multinomial(1)
            return action.data[0,0]          
        else:
            probs = self.model(Variable(torch.from_numpy(state).unsqueeze(0).float()));
            return torch.argmax(probs).item();
        
    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1);
        next_outputs = self.model(batch_next_state).detach().max(1)[0];
        target = self.gamma*next_outputs + batch_reward;
        td_loss = F.smooth_l1_loss(outputs, target);
        readableloss = td_loss.detach().numpy();
        self.optimizer.zero_grad();
        td_loss.backward();
        self.optimizer.step();
        
    def update(self, reward, new_visible_state, action_selected):
        new_state = Variable(torch.from_numpy(new_visible_state).unsqueeze(0).float());
        visiblelaststate = self.last_state.detach().numpy();
        self.memory.push((self.last_state, new_state, torch.LongTensor([int(self.last_action)]), torch.Tensor([self.last_reward])))
        action = self.select_action(new_visible_state);
        if len(self.memory.memory) > 20: #Learning after 20 actions
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(20);
            self.learn(batch_state, batch_next_state, batch_reward, batch_action);
        self.last_action = action_selected;
        self.last_state = new_state
        self.last_reward = reward
        
    def save(self):
        torch.save({'state_dict': self.model.state_dict(),
                    'optimizer' : self.optimizer.state_dict(),
                   }, 'tetris_agent.pth');
        print("Saved agent.");
    
    def load(self):
        if os.path.isfile('tetris_agent.pth'):
            print("=> Loading agent... ");
            checkpoint = torch.load('tetris_agent.pth');
            self.model.load_state_dict(checkpoint['state_dict']);
            self.optimizer.load_state_dict(checkpoint['optimizer']);
            print("Done !");
        else:
            print("No agent found...");