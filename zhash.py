from random import randint
import random
W = 8
H = 8

PIECES = {2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I', 10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

table = []
Piece = 2

# For every cell and every piece in that cell, assign a random number to it
def init_table():
    global table
    for i in range(W):
        for j in range(H):
            for p in range(Piece):
                table[i][j][p] = randint(0,  4294967296)


def hash_state(board):
    global table
    hash = 0
    for r in range(W):
        for c in range(H):
            piece = PIECES[board[r][c]]
            if piece != '-':
                index = table[piece]
                hash ^= table[r][c][index]
    return hash