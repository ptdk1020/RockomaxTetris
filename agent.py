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
        self.fc1 = nn.Linear(input_size, 1000);
        self.fc2 = nn.Linear(1000, 1000);
        self.fc3 = nn.Linear(1000, nb_actions);
        
    def forward(self, state):
        x = F.relu(self.fc1(state));
        x = F.relu(self.fc2(x));
        q_values = F.relu(self.fc3(x))
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
        self.reward_window = [];
        self.model = Brain(input_size, nb_actions);
        self.memory = ReplayMemory(500);
        self.optimizer = optim.Adam(self.model.parameters(), lr = 0.005);
        self.last_state = torch.Tensor(input_size).unsqueeze(0);
        self.last_action = 0;
        self.last_reward = 0;
        
    def select_action(self,state, training = True):
        if(training):
            probs = F.softmax(self.model(Variable(state, volatile = True))*100); # T=100
            action = probs.multinomial(1)
            return action.data[0,0]          
        else:
            probs = self.model(Variable(state, volatile = True));
            return torch.argmax(probs).item();
        
    def update(self, reward, new_state):
        pass;
        
    def save(self):
        torch.save({'state_dict': self.model.state_dict(),
                    'optimizer' : self.optimizer.state_dict(),
                   }, 'tetris_agent.pth');
        print("Saved agent.")
    
    def load(self):
        if os.path.isfile('tetris_agent.pth'):
            print("=> Loading agent... ")
            checkpoint = torch.load('tetris_agent.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("Done !")
        else:
            print("No agent found...")
