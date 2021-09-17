import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable


# Initializing and setting the variance of a tensor of weights
def normalized_columns_initializer(weights, std=1.0):
    out = torch.randn(weights.size())
    out *= std / torch.sqrt(out.pow(2).sum(1).expand_as(out))
    return out

#Brain

class Brain(nn.Module):
    
    def __init__(self, input_size, nb_actions):
        super(Brain, self).__init__();
        self.input_size = input_size;
        self.nb_action = nb_actions;
        self.fc1 = nn.Linear(input_size, 2000);
        self.fc2 = nn.Linear(2000, 500);
        self.fc3 = nn.Linear(500, 128);
        self.fca = nn.Linear(128, nb_actions);
        self.fcv = nn.Linear(128,1);
        self.fcv.weight.data = normalized_columns_initializer(self.fcv.weight.data, 1.0)
        self.fcv.bias.data.fill_(0)
        self.x1 = torch.Tensor([0.1]);
        self.x2 = torch.Tensor([0.1]);
        self.x3 = torch.Tensor([0.1]);
        
    def forward(self, state):
        x = F.prelu(self.fc1(state),self.x1);
        x = F.prelu(self.fc2(x),self.x2);
        x = F.prelu(self.fc3(x),self.x3);
        q_values = self.fca(x);
        v_value = self.fcv(x);
        return q_values, v_value;