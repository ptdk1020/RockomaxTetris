import numpy as np
import random
import game

class Piece(): 
    def __init__(self, piece_type):
        self.x = 0 ;
        self.y = game.height + 2;
        self.data = np.zeros((4,4))
        self.piece_type = piece_type;
        if piece_type == 0:
            self.data = np.array([[1,1],[1,1]]);
        elif piece_type == 1:
            self.data = np.array([[0,0,0],[0,1,0],[1,1,1]]);
        elif piece_type == 2:
            self.data = np.array([[0,0,0],[1,1,0],[0,1,1]]);
        elif piece_type == 3:
            self.data = np.array([[0,0,0],[0,1,1],[1,1,0]]);
        elif piece_type == 4:
            self.data = np.array([[0,0,0],[0,0,1],[1,1,1]]);
        elif piece_type == 5:
            self.data = np.array([[0,0,0],[1,0,0],[1,1,1]]);
        elif piece_type == 6:
            self.data = np.array([[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]]);
        
    def clockwise_rotate(self):
        if self.piece_type == 0:
            return;
        elif self.piece_type == 6:
            newdata = np.zeros((4,4))
            for i in range(0,4):
                for j in range(0,4):
                    x = i - 1.5;
                    y = j - 1.5;
                    newx = y;
                    newy = -x;
                    newdata[(int)(newy + 1.5),(int)(newx + 1.5)] = (int)(self.data[j,i]);
            self.data = newdata;
        else:
            newdata = np.zeros((3,3))
            for i in range(0,3):
                for j in range(0,3):
                    x = i - 1;
                    y = j - 1;
                    newx = y;
                    newy = -x;
                    newdata[(int)(newy + 1),(int)(newx + 1)] = (int)(self.data[j,i]);
            self.data = newdata;            