from kivy.uix.widget import Widget
import numpy as np
import random

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
            self.piece.y -= 1;
            if(self.checkcollision()):
                self.piece.y += 1;
                self.mergepiece();
        #Updating the visible board, first by resetting it.
        self.boardandpiece = np.zeros((2,20,10));
        for i in range(0,10):
            for j in range(0,20):
                self.boardandpiece[0,j,i] = self.board[j,i];
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                if(self.piecey-i < 20):
                    self.boardandpiece[1,self.piece.y-i, self.piece.x+j] = self.active_piece.data[j,i]
        return;
        
    def checkcollision(self, Piece test_piece): #Check if a piece collides with board with its current coordinates
        collisionresult = 0;
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                collisionresult += self.board[test_pice.y-i, test_piece.x+j]*self.active_piece.data[j,i];
        return collisionresult;
        
    def mergepiece(self): #Merge the piece with the board
        self.is_piece_active = False;
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):        
                self.board[self.piece.y-i, self.piece.x+j] = self.active_piece.data[j,i]
        return;