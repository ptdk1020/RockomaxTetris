import numpy as np
import random
from copy import copy

import piece

height = 10;
width = 6;

class Game():
    def __init__(self):
        self.start();
        
    def start(self):
        self.board = np.zeros((height+3,width), dtype="float64") #Game board extends internally above y = 20 to allow pieces to exist there
        self.boardandpiece = np.zeros((2,height,width), dtype = "float64") #3D array.  0 for a dead block, 1 for for a block from the active piece
        self.is_piece_active = False;
        self.game_over = False;
        self.reward = 0;
        self.pieces_list = self.random_list();
        self.total_score = 0;
        self.grace_period = False;
        
    def getReward(self):
        reward =  self.reward;
        self.total_score += reward;
        reward -= self.count_blocks()/100.0;
        self.reward = 0;
        return reward;
    
    def getScore(self):
        return self.total_score;
    
    def count_blocks(self):
        return np.prod(self.boardandpiece[:,:,:]);
    
    def random_list(self):
        newlist = np.array([0])
#        newlist = np.array([0,1,2,3,4,5,6]);
        np.random.shuffle(newlist);
        return newlist;
        
    def update(self, *args):
        if not (self.game_over):
            if(self.grace_period == True):
                self.grace_period = False;
            else:
                self.check_lines();
            if(self.is_piece_active == False):
                self.survival = 0;
                self.is_piece_active = True;
                if(np.size(self.pieces_list) == 0):
                    self.pieces_list = self.random_list();
                self.active_piece = piece.Piece(self.pieces_list[0]);
                self.pieces_list = np.delete(self.pieces_list,0);
            else:
                self.active_piece.y -= 1;
                if(self.checkcollision(self.active_piece)):
                    self.active_piece.y += 1;
                    self.mergepiece();
            self.update_visibleboard()
            self.survival += 1;
            
    def check_lines(self):
        i = 0
        while i < height:
            full = np.prod(self.board[i, :])
            if full == 1:
                self.board[i:-1, :] = self.board[i + 1:, :]
                self.board[height - 1,:] = 0
                self.reward += 1;
            else:
                i += 1

    def update_visibleboard(self):
        #Updating the visible board, first by resetting it.
        self.boardandpiece = np.zeros((2,height,width));
        for i in range(0,width):
            for j in range(0,height):
                self.boardandpiece[0,j,i] = self.board[j,i];
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                if(self.active_piece.y-i < height and self.active_piece.x+j >= 0 and self.active_piece.x+j < width):
                    self.boardandpiece[1,self.active_piece.y-i, self.active_piece.x+j] = self.active_piece.data[j,i]
        return;
        
    def checkcollision(self, test_piece): #Check if a piece collides with board or the edges with its current coordinates
        collisionresult = 0;
        for i in range(0, np.size(test_piece.data,1)):
            for j in range(0,np.size(test_piece.data,0)):
                if(test_piece.y-i < 0 or test_piece.x+j < 0 or test_piece.x+j > width - 1):
                    collisionresult += test_piece.data[j,i];
                else:
                    collisionresult += self.board[test_piece.y-i, test_piece.x+j]*test_piece.data[j,i];        
        return collisionresult;
        
    def mergepiece(self): #Merge the piece with the board
        self.is_piece_active = False;
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                if(self.active_piece.data[j,i] == 1 and self.active_piece.y-i > height - 1):
                    self.game_over = True;
                if(self.active_piece.data[j,i] == 1 and self.board[self.active_piece.y-i, self.active_piece.x+j] == 0):
                    self.board[self.active_piece.y-i, self.active_piece.x+j] = self.active_piece.data[j,i];
        self.reward += (height - self.active_piece.y)/100.0;
        if(np.size(self.pieces_list) == 0):
            self.pieces_list = self.random_list();
        self.active_piece = piece.Piece(self.pieces_list[0]);
        self.pieces_list = np.delete(self.pieces_list,0);
        return;

    def left(self):
        new_piece = copy(self.active_piece);
        new_piece.x -= 1
        # if no collision, move active piece
        if not self.checkcollision(new_piece):
            self.active_piece.x -= 1
            self.reward += 0.002 * (height - self.active_piece.y);
        else:
            self.reward -= 0.001;
        return

    def right(self):
        new_piece = copy(self.active_piece);
        new_piece.x += 1
        # if no collision, move active piece
        if not self.checkcollision(new_piece):
            self.active_piece.x += 1
            self.reward += 0.002 * (height - self.active_piece.y);
        else:
            self.reward -= 0.001;
        return

    def up(self):
        new_piece = copy(self.active_piece)
        new_piece.clockwise_rotate()
        if not self.checkcollision(new_piece):
            self.active_piece.clockwise_rotate()
        return

    def down(self):
        new_piece = copy(self.active_piece)
        new_piece.y -= 1
        if not self.checkcollision(new_piece):
            self.reward += 0.002 * (height - self.active_piece.y);
            self.active_piece = new_piece;
        else:
            self.mergepiece()
