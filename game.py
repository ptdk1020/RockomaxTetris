import numpy as np
import random

import piece

class Game():
    def __init__(self):
        self.board = np.zeros((23,10)) #Game board extends above y = 20 to allow pieces to exist there
        self.is_piece_active = False;
    def update(self):
        if(self.is_piece_active == False):
            self.active_piece = piece.Piece(random.randint(0,6));
            self.piecex = 4;
            self.piecey = 22;
        else:
            self.piecey -= 1;
            if(self.checkcollision()):
                self.piecey += 1;
                self.mergepiece();
              
        return;
        
    def checkcollision(self): #Check if a piece collides with board with its current coordinates
        collisionresult = 0;
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):
                collisionresult += self.board[self.piecey-i, self.piecex-j]*self.active_piece.data[j,i];
        return collisionresult;
        
    def mergepiece(self): #Merge the piece with the board
        for i in range(0, np.size(self.active_piece.data,1)):
            for j in range(0,np.size(self.active_piece.data,0)):        
                self.board[self.piecey-i, self.piecex-j] = self.active_piece.data[j,i]
        return;
        
    def render(self):
        return;
        
game = Game();
game.update();
print(game.checkcollision())