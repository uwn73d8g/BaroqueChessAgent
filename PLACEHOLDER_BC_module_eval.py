import BC_state_etc as BC_state
import PLACEHOLDER_BC_Player as player
NEIGHBOR = (-1, 0, 1)
# piece values are referenced from chess game
# pawn 100, Bishop 340, Rook 500, Knight 325, Queen 900, King 10000, Imitator
# 0 empty, 1 pincer, 2 coordinator, 3 leaper, 4 imitator, 5 withdrawer, 6 king, 7:freezer
PIECE_VALUES = {0: 0, 1: 100, 2: 500, 3: 325, 4: 325, 5: 900, 6: 10000, 7: 800}
CORSS_DIR=((1,0),(0,1),(-1,0),(0,-1))
BOARDROW = 8
BOARDCOL = 8

EMPTY=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
       [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_PINCER_FACTOR=[
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, 0.5, 1.0,  0.0,  0.0, 1.0, 0.5,  0.5],
        [0.5,  1.0, 1.0,  2.0, 2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]


WHITE_COOR_FACTOR=[[  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ 0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5],
    [ 0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5],
    [ 0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5],
    [ 0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5],
    [ 0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]]

WHITE_LEAPER_FACTOR=[[ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

WHITE_IMITATOR_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_WITHDRAWER_FACTOR=[[ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

WHITE_KING_FACTOR=[[ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]]

WHITE_FREEZER_FACTOR=[[ -2.0, 4.0, 5.0, 4.5, 4.5, 4.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

WHITE_PIECE_FACTORS=[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                     EMPTY, EMPTY, EMPTY]

BLACK_PIECE_FACTORS=[[i[::-1] for i in EMPTY[::-1]], [i[::-1] for i in WHITE_PINCER_FACTOR[::-1]], [i[::-1] for i in WHITE_COOR_FACTOR[::-1]],
                     [i[::-1] for i in WHITE_LEAPER_FACTOR[::-1]], [i[::-1] for i in WHITE_IMITATOR_FACTOR[::-1]],
                     [i[::-1] for i in WHITE_WITHDRAWER_FACTOR[::-1]], [i[::-1] for i in WHITE_KING_FACTOR[::-1]],
                     [i[::-1] for i in WHITE_FREEZER_FACTOR[::-1]]]

w_king_pos=None
b_king_pos=None

def static_eval(state):
    global w_king_pos, b_king_pos
    white=0
    black=0
    if state is None:return 0
    for i, row in enumerate(state.board):
        for j, tile in enumerate(row):
            isWhite = tile % 2 == 1
            if tile != 0:
                # calculate how many piece are remained on board
                if isWhite: white+=(PIECE_VALUES[tile//2]+WHITE_PIECE_FACTORS[tile//2][i][j])
                else: black+=(PIECE_VALUES[tile//2]+BLACK_PIECE_FACTORS[tile//2][i][j])

                # pincer next move capture
                if isWhite: white+=find_pin(state, i, j, 1)
                else: black+=find_pin(state, i, j, 0)

                # check how many pieces are frozen
                if tile // 2 == 7:
                    if isWhite:
                        for neighbor in get_neighbor(i,j):
                            tile_temp=state.board[neighbor[0]][neighbor[1]]
                            if tile_temp !=0 and tile % 2 != 1: white+=PIECE_VALUES[tile_temp // 2]
                    else:
                        for neighbor in get_neighbor(i,j):
                            tile_temp=state.board[neighbor[0]][neighbor[1]]
                            if tile_temp !=0 and tile % 2 == 1: white+=PIECE_VALUES[tile_temp // 2]

                # check if king is in save position
                # saver, higher score
                if tile // 2 == 6:
                    if isWhite:
                        w_king_pos=(i,j)
                        for neighbor in get_neighbor(i, j):
                            tile_temp = state.board[neighbor[0]][neighbor[1]]
                            if tile_temp !=0 and tile % 2 != 1: white-=PIECE_VALUES[tile_temp // 2]
                    else:
                        b_king_pos=(i,j)
                        for neighbor in get_neighbor(i, j):
                            tile_temp = state.board[neighbor[0]][neighbor[1]]
                            if tile_temp !=0 and tile % 2 != 1: black-=PIECE_VALUES[tile_temp // 2]

    return white - black

def find_pin(state, i, j, side):
    '''

    :param state: state of the board
    :param i: row index
    :param j:col index
    :return: return a score of how many pieces are adjacent to friendly peice
    '''
    score=0
    for dir in CORSS_DIR:
        new_row=i+dir[0]
        new_col=j+dir[1]
        if new_row >=0 and new_row < BOARDCOL and new_col >=0 and new_col<BOARDROW:
            tile=state.board[new_row][new_col]
            if tile !=0 and tile % 2 != side:
                score+=PIECE_VALUES[tile//2]

    return score



def get_neighbor(i, j):
    '''

    :param i: row index
    :param j: column index
    :return: list of tuples of possible neighbor location of given position
    '''
    neighbors = []

    for row_factor in NEIGHBOR:
        for col_factor in NEIGHBOR:
            neighbor_row = row_factor + i
            neighbor_col = col_factor + j
            if neighbor_col == j and neighbor_row == i:
                continue
            else:
                if neighbor_col >=0 and neighbor_col <  BOARDCOL and neighbor_row >= 0 and neighbor_row < BOARDROW:
                    neighbors.append((neighbor_row, neighbor_col))

    return neighbors


