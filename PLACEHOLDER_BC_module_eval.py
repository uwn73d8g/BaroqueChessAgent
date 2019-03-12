import BC_state_etc as BC_state

NEIGHBOR = (-1, 0, 1)
# piece values are referenced from chess game
# pawn 100, Bishop 340, Rook 500, Knight 325, Queen 900, King 10000, Imitator
# 0 empty, 1 pincer, 2 coordinator, 3 leaper, 4 imitator, 5 withdrawer, 6 king, 7:freezer
PIECE_VALUES = {0: 0, 1: 100, 2: 500, 3: 325, 4: 325, 5: 900, 6: 10000, 7: 800}
CORSS_DIR=((1,0),(0,1),(-1,0),(0,-1))
BOARDROW = 8
BOARDCOL = 8

WHITE_PINCER_FACTOR=[
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]


WHITE_COOR_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_LEAPER_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_IMITATOR_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_WITHDRAWER_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_KING_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_FREEZER_FACTOR=[[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

WHITE_PIECE_FACTORS=[WHITE_PINCER_FACTOR, WHITE_PINCER_FACTOR, WHITE_COOR_FACTOR, WHITE_LEAPER_FACTOR, WHITE_IMITATOR_FACTOR,
                     WHITE_WITHDRAWER_FACTOR, WHITE_KING_FACTOR, WHITE_FREEZER_FACTOR]

BLACK_PIECE_FACTORS=[[i[::-1] for i in WHITE_PINCER_FACTOR[::-1]], [i[::-1] for i in WHITE_PINCER_FACTOR[::-1]], [i[::-1] for i in WHITE_COOR_FACTOR[::-1]],
                     [i[::-1] for i in WHITE_LEAPER_FACTOR[::-1]], [i[::-1] for i in WHITE_IMITATOR_FACTOR[::-1]],
                     [i[::-1] for i in WHITE_WITHDRAWER_FACTOR[::-1]], [i[::-1] for i in WHITE_KING_FACTOR[::-1]],
                     [i[::-1] for i in WHITE_FREEZER_FACTOR[::-1]]]


def static_eval(state):
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
                if tile % 2 == 1:
                    pining_count = find_pin(state, i, j)
                    if isWhite: white+=1
                    else: black+=1

    return white - black

def find_pin(state, i, j):
    '''

    :param state:
    :param i:
    :param j:
    :return:
    '''
    count=0
    for dir in CORSS_DIR:
        k=1
        new_row=i+k*dir[0]
        new_col=j+k*dir[1]
        # while new_row


# def static_eval(board, side):
#     score = 0
#
#     white_score = 0
#     black_score = 0
#     for i, row in enumerate(board):
#         for j, piece in enumerate(row):
#
#
#             # calculate how many friendly pieces are still in the board
#             if piece % 2 == 0:
#                 score += PIECE_VALUES[piece // 2]
#
#
#             # calculate how many enemy's pieces are frozen by friendly freezer
#             if piece // 2 == 7:
#                 neighbors = get_neighbors(i, j)
#                 for neighbor in neighbors:
#                     cur_piece = board[neighbor[0]][neighbor[1]]
#                     if cur_piece % 2 == side:
#                         score += PIECE_VALUES[cur_piece // 2]
#
#
#     return score



def get_neighbor(i, j):
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


