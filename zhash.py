# import random
# # def init_table():
# zobTable = [[[random.randint(1,2**64 - 1) for i in range(12)]for j in range(8)]for k in range(8)]
# # for i in zobTable:
# #     for j in i:
# #         for k in j:
# #             print(k),
# #         print 


# def hash_state(board):
#     h = 0
#     for i in range(8):
#         for j in range(8):
#             print(board.board[i][j])
#             if board.board[i][j] != 0:
#                 piece = board.board[i][j]
#                 # print(piece)
#                 h ^= zobTable[i][j][piece % 2]
#     return h

import BC_state_etc as BC
from random import randint
import math

PIECES = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

ZOBRIST_INDEXES = {'p':0, 'P':1, 'c':2, 'C':3, 'l':4, 'L':5, 'i':6, 'I':7,
  'w':8, 'W':9, 'k':10, 'K':11, 'f':12, 'F':13, }
ZOBRIST_NUMBERS = []
ZHASH = None

TRANSPOSITION_TABLE = []
TABLE_SIZE = 0

INITIAL = BC.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

BOARD_ONE_MOVE = BC.parse('''
c l i w k i l f
p p p p p p p -
- - - - - - - p
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

def init_zhash():
    global ZOBRIST_NUMBERS
    for r in range(8):
        ZOBRIST_NUMBERS.append([])
        for c in range(8):
            ZOBRIST_NUMBERS[r].append([])
            for p in range(14):
                ZOBRIST_NUMBERS[r][c].append(0)
    for i in range(8):
        for j in range(8):
            for p in range(14):
                ZOBRIST_NUMBERS[i][j][p] = \
                    randint(0, math.pow(2,64))

def zhash(board):
    global ZOBRIST_NUMBERS
    hash = 0
    for r in range(8):
        for c in range(8):
            piece = PIECES[board[r][c]]
            if piece != '-':
                #print(piece)
                index = ZOBRIST_INDEXES[piece]
                hash ^= ZOBRIST_NUMBERS[r][c][index]
                #print(hash)
    return hash

def update_zhash_piece_movement(start, dest, piece, hash):
    piece = PIECES[piece]
    index = ZOBRIST_INDEXES[piece]
    hash ^= ZOBRIST_NUMBERS[start[0]][start[1]][index]
    hash ^= ZOBRIST_NUMBERS[dest[0]][dest[1]][index]
    return hash

def update_zhash_remove_piece(location, piece, hash):
    piece = PIECES[piece]
    index = ZOBRIST_INDEXES[piece]
    hash ^= ZOBRIST_NUMBERS[location[0]][location[1]][index]
    return hash


class Hash_Entry:
    def __init__(self, key, eval, type, ply, best_move):
        self.key = key
        self.eval = eval
        self.type = type
        self.ply = ply
        self.best_move = best_move


'''prepare("what up")
#initZhash()
hash = zHash(INITIAL)
print(hash)
hash2 = zHash(INITIAL)
print(hash2)
updated_hash = update_zhash_piece_movement((1,7), (2,7), 2, hash2)
hash3 = zHash(BOARD_ONE_MOVE)
print("\n")
print(hash3)
print(updated_hash)
print(hash)
print(hash2)'''