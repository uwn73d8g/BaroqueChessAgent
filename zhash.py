
import random
zobTable = [[[random.getrandbits(64) for i in range(12)]for j in range(8)]for k in range(8)]

def table():
    return zobTable
    
for i in zobTable:
    for j in i:
        for k in j:
            print(k),
        print 

# Returns the hash value for a given state
# def hash_state(state):
#     global zobTable
#     h = 0
#     board = state.board
#     for row in range(0, 7):
#         for column in range(0, 7):
#             piece = board[row][column]
#             if piece != 0:
#                 # print(row)
#                 # print(column)
#                 print(piece)
#                 h ^= zobTable[row][column][piece]
#     return h
INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}
def hash_state(board):
    h = 0
    for i in range(8):
        for j in range(8):
            # print(i)
            # print(j)
            # print(board.board[i][j])
            num = board.board[i][j]
            if num != '-':
                piece = INIT_TO_CODE.get(num)
                # print(i)
                # print(j)
                if piece is None:
                    break
                h ^= zobTable[i][j][piece]
                # print(h)
            # else
    return h

# def indexing(piece):
    ''' mapping each piece to a particular number'''
    if (piece=='P'):
        return 0
    if (piece=='N'):
        return 1
    if (piece=='B'):
        return 2
    if (piece=='R'):
        return 3
    if (piece=='Q'):
        return 4
    if (piece=='K'):
        return 5
    if (piece=='p'):
        return 6
    if (piece=='n'):
        return 7
    if (piece=='b'):
        return 8
    if (piece=='r'):
        return 9
    if (piece=='q'):
        return 10
    if (piece=='k'):
        return 11
    else:
        return 0

# def computeHash(board):
#     h = 0
#     for i in range(8):
#         for j in range(8):
#            # print board[i][j]
#             if board[i][j] != '-':
#                 piece = indexing(board[i][j])
#                 h ^= zobTable[i][j][piece]
#     return h
# def main():
#     # Upper Case are white pieces
#     # Lower Case are black pieces

#     # a [8][8] format board
#     board = [
#         ['-', '-', '-', 'K', '-', '-', '-', '-'],
#         ['-', 'R', '-', '-', '-', '-', 'Q', '-'],
#         ['-', '-', '-', '-', '-', '-', '-', '-'],
#         ['-', 'P', '-', '-', '-', '-', 'p', '-'],
#         ['-', '-', '-', '-', '-', 'p', '-', '-'],
#         ['-', '-', '-', '-', '-', '-', '-', '-'],
#         ['p', '-', '-', '-', 'b', '-', '-', 'q'],
#         ['-', '-', '-', '-', 'n', '-', '-', 'k']
#     ]

#     hashValue = computeHash(board)
#     print "Current Board is :"
#     for i in board:
#         for j in i:
#             print j,
#         print

#     print "\nThe Current hash is : ",hashValue,"\n"

#     # an exaple of channge in game state and how it affects the hashes

#     # move white Rook to at a new postion in right
#     piece = board[1][1]

#     board[1][1] = '-'
#     hashValue ^= zobTable[1][1][indexing(piece)]

#     board[3][1] = piece
#     hashValue ^= zobTable[3][1][indexing(piece)]
#     print "The new board is :"
#     for i in board:
#         for j in i:
#             print j,
#         print

#     print "\nHash after the move is : ",hashValue,"\n"

# if __name__ == "__main__":
#     main()

