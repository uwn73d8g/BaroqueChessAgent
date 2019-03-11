'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import PLACEHOLDER_BC_module_eval as eval
import time
from random import randint

TURN = 0
zobristnum = []
mySide = 'W'
rows = 8
columns = 8
K = 8
S = 64
P = 2
NUM_ROWS = 8
NUM_COLS = 8


ALL_DIRECTION = {BC.NORTH:(0,1), BC.EAST:(1,0), BC.SOUTH:(0, -1), BC.WEST:(-1, 0), BC.NW:(-1, 1), BC.NE:(1,1), BC.SW:(-1, -1), BC.SE:(1, -1)}

def valid_moves(board):
    whose_turn = board.whose_move
    moves = []
    for i, row in enumerate(board.board):
        for j, tile in enumerate(row):
            if tile != 0 and tile % 2 == whose_turn and not_frozen(board,i,j, whose_turn):
#                 pincer movement
                if tile // 2 == 0:
                    moves+=pincer_moves(board, i, j)


def pincer_moves(state, row, col):
    '''
    :param state: state of the board
    :param row: row index
    :param col: col index
    :return: a list of possible states of board generated by possible pincer moves
    '''
    moves = []
    for dir_key in range(4):
        dir = ALL_DIRECTION[dir_key]
        k = 1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                pincer_capture(new_state, (new_row, new_col))


def pincer_capture(state, cur_pos):
    '''
    check if pincer moves capture any pieces and return a new state
    :param state: state of the board
    :param cur_pos: tuple of the position
    :return: new state of after pincer captures
    '''
    new_row = cur_pos[0]
    new_col = cur_pos[1]

    for dir_key in range(4):
        dire = ALL_DIRECTION[dir_key]
        possible_enemy_pos = (new_row+dire[0], new_col+dire[1])
        possible_enemy_tile = state.board[possible_enemy_pos[0]][possible_enemy_pos[1]]
        hasEnemy = possible_enemy_tile != 0 and possible_enemy_tile % 2 != state.whose_move

        possible_firendly_pos = (new_row+dire[0]*2, new_col+dire[1]*2)
        possible_firendly_tile = state.board[possible_firendly_pos[0]][possible_firendly_pos[1]]
        hasFirendly = possible_firendly_tile != 0 and possible_firendly_tile % 2 != state.whose_move

        if hasEnemy and hasFirendly and possible_firendly_pos[0] >=0 and possible_firendly_pos[0] < NUM_COLS and possible_firendly_pos[1] >=0 and possible_firendly_pos < NUM_ROWS:
            state.board[possible_enemy_pos[0]][possible_enemy_pos[1]] == 0

    return BC.BC_state(state.board, state.whose_move)




def not_frozen(board, row, col):
    neighbors = eval.get_neighbors(row, col)
    for neighbor in neighbors:
        piece = board.board[neighbor[0]][neighbor[1]]
        if piece // 2 == 7 and piece % 7 != board.whose_move:
            return False
    return True

def move_piece(state, pre_pos, cur_pos):
    new_state = BC.BC_state(state.board, state.whose_move)
    new_state.board[cur_pos[0]][cur_pos[1]] = new_state.board[pre_pos[0]][pre_pos[1]]
    new_state.board[pre_pos[0]][pre_pos[1]] = 0
    return new_state



def alpha_beta_pruning(current_depth, max_ply, current_state, turn, alpha, beta, isTimed, default_move, start_time,
                       time_limit):
    global state_expanded_count, maximum_depth, cutoff_count, state_evaluate_count, USE_DEFAULT_ORDER
    if current_depth > maximum_depth:
        maximum_depth = current_depth

    moves = current_state.get_moves(turn)
    best_move = current_state
    if isTimed:
        if time.time() - start_time >= time_limit * 0.9:
            return current_state
        if not moves or current_depth == max_ply:
            state_evaluate_count += 1
            return current_state
        state_expanded_count += 1

        for move in moves:
            state = alpha_beta_pruning(current_depth + 1, max_ply, move, turn, alpha, beta, start_time,
                                       isTimed, default_move, time_limit)
            eval_val = state.static_eval()
            if turn == 'W':
                if eval_val > alpha:
                    alpha = eval_val
                    best_move = state
            else:
                if eval_val < beta:
                    beta = eval_val
                    best_move = state

            if alpha >= beta:
                cutoff_count += 1
                return best_move

        return best_move

    else:
        if not moves or current_depth == max_ply:
            state_evaluate_count += 1
            return current_state

        state_expanded_count += 1

        for move in moves:
            state = alpha_beta_pruning(current_depth + 1, max_ply, move, turn, alpha, beta, start_time,
                                       isTimed, default_move, time_limit)
            eval_val = state.static_eval()
            if turn == 'W':
                if eval_val > alpha:
                    alpha = eval_val
                    best_move = state
            else:
                if eval_val < beta:
                    beta = eval_val
                    best_move = state

            if alpha >= beta:
                cutoff_count += 1
                return best_move

        return best_move


def makeMove(currentState, currentRemark, timelimit):
    global TURN
    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    new_utterance = utterance()
    TURN += 1
    return [[move, newState], new_utterance]


def nickname():
    return "Spiderman"


def introduce():
    return "I am Spiderman. I am a powerful player. I will beat you up."


def prepare(player2Nickname):
    global mySide, P, zobristnum
    mySide = mySide
    zobristnum = [[0] * P for i in range(S)]
    for i in range(S):
        for j in range(P):
            zobristnum[i][j] = randint(0, 100000000)
    return "OK"


def zhash(board):
    val = 0
    for i in range(0, rows):
        for j in range(0, columns):
            piece = None
            if board[i][j] != '-' and board[i][j].isupper():
                piece = 0
            if board[i][j] != '-' and board[i][j].islower():
                piece = 1
            if piece is not None:
                val ^= zobristnum[i * columns + j][piece]
    return val


def utterance():
    utterances = ["You are way too weak!",
                  "Are you even trying?",
                  "Use your brain!",
                  "Five-year-old knows better than you!",
                  "Such a boring match.",
                  "Come on! Such a horrible choice.",
                  "This is the best you can do? So disappointing!",
                  "I have never met anyone that's as weak as you!",
                  "Such a waste of time!",
                  "I will show you my power!",
                  "Do you really know how to play this game?"]
    return utterances[TURN % 11]
