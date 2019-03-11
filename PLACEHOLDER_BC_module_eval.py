import BC_state_etc as BC_state
DIAGONAL_MOVES = [(1,-1), (1,1), (-1,1), (-1,-1)]
ROOK_MOVES = [(0,1), (1,0), (-1,0), (0,-1)]
QUEEN_MOVES = ROOK_MOVES + DIAGONAL_MOVES

NEIGHBOR = (-1, 0, 1)

PIECE_VALUES = {0: 0, 1: 1, 2: 2, 3: 5, 4: 5, 5: 2, 6: 10000, 7: 8}
# weights = {'piece': 1, 'freezing': 1, 'withdraw': 1}
#
# DIAGONAL_MOVES = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
# ROOK_MOVES = [(0, 1), (1, 0), (-1, 0), (0, -1)]
# QUEEN_MOVES = ROOK_MOVES + DIAGONAL_MOVES

BOARDROW = 8
BOARDCOL = 8
def static_eval(board, side):
    score = 0

    white_score = 0
    black_score = 0
    for i, row in enumerate(board):
        for j, piece in enumerate(row):


            # calculate how many friendly pieces are still in the board
            if piece % 2 == 0:
                score += PIECE_VALUES[piece // 2]


            # calculate how many enemy's pieces are frozen by friendly freezer
            if piece // 2 == 7:
                neighbors = get_neighbors(i, j)
                for neighbor in neighbors:
                    cur_piece = board[neighbor[0]][neighbor[1]]
                    if cur_piece % 2 == side:
                        score += PIECE_VALUES[cur_piece // 2]


    return score


def get_neighbors(i, j):
    neighbors = []

    for row_factor in NEIGHBOR:
        for col_factor in NEIGHBOR:
            neighbor_row = row_factor + i
            neighbor_col = col_factor + j
            if neighbor_col != j and neighbor_row != i:
                if neighbor_col >=0 and neighbor_col <  BOARDCOL and neighbor_row >= 0 and neighbor_row < BOARDROW:
                    neighbors.append((neighbor_row, neighbor_col))

    return neighbors



# def get_neighbors(board, i, j, directions):
#     num_rows = len(board.board)
#     num_cols = len(board.board[0])
#
#     neighbors = []
#
#     for (dr, dc) in directions:
#         new_row = i + dr
#         new_col = j + dc
#         if new_row >= 0 and new_col >= 0 and new_row < num_rows and new_col < num_cols:
#             neighbors.append(board.board[i + dr][j + dc])
#
#     return neighbors
