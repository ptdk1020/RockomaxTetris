import numpy as np
import random
from copy import copy

import piece

class Game():
    def __init__(self):
        self.board = np.zeros((23,10)) #Game board extends internally above y = 20 to allow pieces to exist there
        self.boardandpiece = np.zeros((2,20,10)) #3D array.  0 for a dead block, 1 for for a block from the active piece
        self.is_piece_active = False;
        
    def update(self, *args):
        if(self.is_piece_active == False):
            self.is_piece_active = True;
            self.active_piece = piece.Piece(random.randint(0,6));
        else:
            self.active_piece.y -= 1;
            if(self.checkcollision(self.active_piece)):
                self.active_piece.y += 1;
                self.mergepiece();
        self.update_visibleboard()

    def update_visibleboard(self):
        #Updating the visible board, first by resetting it.
        self.boardandpiece = np.zeros((2,20,10));
        for i in range(0,10):
            for j in range(0,20):
                self.boardandpiece[0,j,i] = self.board[j,i];
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                if(self.active_piece.y-i < 20):
                    self.boardandpiece[1,self.active_piece.y-i, self.active_piece.x+j] = self.active_piece.data[j,i]
        return;
        
    def checkcollision(self, test_piece): #Check if a piece collides with board or the edges with its current coordinates
        collisionresult = 0;
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                if(test_piece.y-i < 0 or test_piece.x+j < 0 or test_piece.x+j > 9):
                    collisionresult += self.active_piece.data[j,i];
                else:
                    collisionresult += self.board[test_piece.y-i, test_piece.x+j]*self.active_piece.data[j,i];        
        
        return collisionresult;
        
    def mergepiece(self): #Merge the piece with the board
        self.is_piece_active = False;
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                if(self.board[self.active_piece.y-i, self.active_piece.x+j] == 0):
                    self.board[self.active_piece.y-i, self.active_piece.x+j] = self.active_piece.data[j,i]
        return;

    def left(self):
        new_piece = copy(self.active_piece);
        new_piece.x -= 1
        # if no collision, move active piece
        if not self.checkcollision(new_piece):
            self.active_piece.x -= 1
        return

    def right(self):
        new_piece = copy(self.active_piece);
        new_piece.x += 1
        # if no collision, move active piece
        if not self.checkcollision(new_piece):
            self.active_piece.x += 1
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
            self.active_piece.y -= 1
        else:
            self.mergepiece()
