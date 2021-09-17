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

import model
    
class A2C(): #advantage actor-critic
    def __init__(self, main_model, gamma):
        self.gamma = gamma;
        self.model = main_model;
        self.optimizer = optim.Adam(self.model.parameters(), lr = 0.001); #Learning rate 0.001
        self.values = []
        self.log_probs = []
        self.rewards = []
        self.entropies = []
        self.states = []
        
    def clear_memory(self):
        self.values = []
        self.log_probs = []
        self.rewards = []
        self.entropies = []
        self.states = []
        
    def select_action(self,state, training = True):
        if(training):
            actors, critic = self.model(Variable(torch.from_numpy(state).unsqueeze(0).float()));
            prob = F.softmax(actors,dim=1);
            log_prob = F.log_softmax(actors,dim=1);
            entropy = -(log_prob * prob).sum(1);
            self.entropies.append(entropy);
            action = prob.multinomial(1).data;
            log_prob = log_prob.gather(1, Variable(action));
            self.values.append(critic);
            self.log_probs.append(log_prob);
            action = prob.multinomial(1);
            self.last_action = action;
            self.states.append(state);
            return action.data[0,0]         
        else:
            prob, _ = self.model(Variable(torch.from_numpy(state).unsqueeze(0).float()));
            return torch.argmax(prob).item();
        
    def learn(self, state):
        _, value = self.model(Variable(torch.from_numpy(state).unsqueeze(0).float()));
        R = value.data;
        self.values.append(Variable(R))
        
        policy_loss = 0;
        value_loss = 0;
        entropy_loss = 0;
        R = Variable(R)
        for i in reversed(range(len(self.rewards))):
            R = self.gamma * R + self.rewards[i]
            advantage = R - self.values[i]
            
            readablevalues = self.values[i].detach().numpy()
            readableR = R.detach().numpy()
            readableadvantage = advantage.detach().numpy()
            
            value_loss = value_loss + 0.5 * advantage.pow(2)
            policy_loss = policy_loss - self.log_probs[i] * advantage.detach();
            entropy_loss = entropy_loss - 0.01 * self.entropies[i]
        
        self.optimizer.zero_grad()
        (policy_loss + 0.5 * value_loss + entropy_loss).backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 40)
        self.optimizer.step()
        self.clear_memory();
       
    def update(self, reward):
        self.rewards.append(reward);
       
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
