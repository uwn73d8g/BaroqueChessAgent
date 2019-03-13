'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import random
import time
from random import randint

import BC_state_etc as BC
import PLACEHOLDER_BC_module_eval as eval
import zhash as hash
# from zhash import hash_state
# hash.init_table()
TURN = 0
NUM_ROWS = 8
NUM_COLS = 8
times_pruned = 0
retrieved = 0
states_evaluated = 0
min_eval = float("inf")
max_eval = float("-inf")
 
ALL_DIRECTION = {BC.NORTH: (-1, 0), BC.SOUTH: (1, 0), BC.WEST: (0, -1), BC.EAST: (0, 1),
                 BC.NW: (-1, -1), BC.NE: (-1, 1), BC.SW: (1, -1), BC.SE: (1, 1)}

# check for valid moves and return a data structure containing all possible valid moves


def valid_moves(state):
    # check for invalid state
    if state is None:
        return []
    board = BC.BC_state(state.board, state.whose_move)
    moves = []
    for i, row in enumerate(board.board):
        for j, tile in enumerate(row):
            # make sure the cell is nonempty and is occupied by a piece owned by whoever's turn current turn
            if tile != 0 and tile % 2 == board.whose_move and not_frozen(board, (i, j)):
                if tile // 2 == 1:
                    # pincer movement
                    moves += pincer_moves(board, i, j)
                elif tile // 2 == 2:
                    # coordiantor movement
                    moves += coordinator_moves(board, i, j)
                elif tile // 2 == 3:
                    # eaper movement
                    moves += leaper_moves(board, i, j)
                elif tile // 2 == 4:
                    # IMITATOR movement
                    moves += imitator_moves(board, i, j)
                elif tile // 2 == 5:
                    # WITHDRAWER movement
                    moves += withdrawer_moves(board, i, j)
                elif tile // 2 == 6:
                    # King movement
                    moves += king_moves(board, i, j)
                else:
                    # freezer movement
                    moves += freezer_moves(board, i, j)
    return moves

# returns all possible freezer moves at a given row and col
def freezer_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves = []
    for dir_key in range(8):
        dire = ALL_DIRECTION[dir_key]
        k = 1
        new_row = row + k*dire[0]
        new_col = col + k*dire[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                moves.append(move_piece(state, (row, col), (new_row, new_col)))
                k += 1
                new_row = row + k * dire[0]
                new_col = col + k * dire[1]
            else:
                break
    return moves

# returns all possible king moves at a given row and col
def king_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves = []
    for dir_key in range(8):
        dire = ALL_DIRECTION[dir_key]
        new_row = row + dire[0]
        new_col = col + dire[1]
        # Since the king captures when it moves, we only check once
        if new_row >= 0 and new_row < NUM_COLS and new_col >= 0 and new_col < NUM_ROWS and (state.board[new_row][new_col] == 0 or (state.board[new_row][new_col] != 0 and state.board[new_row][new_col] % 2 != state.whose_move)):
            if king_check(state, (new_row, new_col)):
                moves.append(move_piece(state, (row, col), (new_row, new_col)))
    return moves

# returns all possible withdrawer moves at a given row and col
def withdrawer_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves = []
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        k = 1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(withdrawer_capture(new_state, (row, col), dir))
                k += 1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else:
                break

    return moves

# returns the state after the withdrawer's capture
def withdrawer_capture(state, pre_pos, dir):
    '''

    :param state:
    :param pre_pos:
    :param dir:
    :return:
    '''
    oppo_dir = (-1*dir[0], dir[1]*-1)
    if oppo_dir[0]+pre_pos[0] >= 0 and oppo_dir[0]+pre_pos[0] < NUM_COLS and oppo_dir[1]+pre_pos[1] >= 0 and oppo_dir[1]+pre_pos[1] < NUM_ROWS and state.board[oppo_dir[0]][oppo_dir[1]] != 0 and state.board[oppo_dir[0]][oppo_dir[1]] % 2 != state.whose_move:
        new_state = BC.BC_state(state.board, state.whose_move)
        new_state.board[oppo_dir[0]+pre_pos[0]][oppo_dir[1]+pre_pos[1]] = 0
        return new_state
    return BC.BC_state(state.board, state.whose_move)

# returns all possible leaper moves at a given row and col
def leaper_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves = []
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        possible_capture = leaper_capture(state, (row, col), dir)
        if possible_capture != state:
            moves.append(leaper_capture(state, (row, col), dir))
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        k = 1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(new_state)
                k += 1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else:
                break
    return moves

# returns the state after the leaper's capture
def leaper_capture(state, cur_pos, dir):
    '''

    :param state: state of the board
    :param cur_pos: current position of the tile
    :param dir: direction of the leap
    :return: return a modified state after capture.
    '''
    hasSpace = cur_pos[0] + 2*dir[0] >= 0 and cur_pos[0] + 2 * \
        dir[0] < NUM_COLS and cur_pos[1] + 2 * \
        dir[1] >= 0 and cur_pos[1] + 2 * dir[1] < NUM_ROWS
    hasEnemy = False
    hasEmpty = False
    if hasSpace:
        possible_enemy_tile = state.board[cur_pos[0]+dir[0]][cur_pos[1]+dir[1]]
        hasEnemy = possible_enemy_tile != 0 and possible_enemy_tile % 2 != state.whose_move

        possible_empty_tile = state.board[cur_pos[1] +
                                          dir[1]*2][cur_pos[1]+dir[1]*2]
        hasEmpty = possible_empty_tile == 0

        if hasSpace and hasEnemy and hasEmpty:
            new_state = move_piece(
                state, cur_pos, (cur_pos[0]+dir[0]*2, cur_pos[1]+dir[1]*2))
            new_state.board[cur_pos[0]+dir[0]][cur_pos[1]+dir[1]] = 0
            return new_state
    return BC.BC_state(state.board, state.whose_move)
    # if cur_pos[0] + 2*dir[0]>=0 and cur_pos[0] + 2 * dir[0] < NUM_COLS and cur_pos[1] + 2*dir[1]>=0 and cur_pos[1] + 2 * dir[1] < NUM_ROWS:

# returns all possible coordinator moves at a given row and col
def coordinator_moves(state, row, col):
    '''

    :param state: state of the board
    :param row: current row index
    :param col: column index
    :return: return a list of states of coordinator possible move
    '''

    moves = []
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        k = 1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(coordinator_capture(
                    new_state, (new_row, new_col)))
                k += 1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else:
                break

    return moves

# returns the state after the coordinator's capture
def coordinator_capture(state, cur_pos):
    '''

    :param state: state of the board
    :param cur_pos: current piece position
    :return: if can capture, return a modified state, otherwise return original state
    '''
    king_pos = get_king_pos(state, state.whose_move)
    if king_pos:
        coor1 = state.board[cur_pos[0]][king_pos[1]]
        coor2 = state.board[king_pos[0]][cur_pos[1]]
        if coor1 != 0 and coor1 % 2 != state.whose_move:
            state.board[cur_pos[0]][king_pos[1]] = 0
        if coor2 != 0 and coor2 % 2 != state.whose_move:
            state.board[king_pos[0]][cur_pos[1]] = 0
    return state

# returns the king's location
def get_king_pos(state, turn):
    '''

    :param state: state of the board
    :param turn: 0 or 1, whose turn
    :return: a tuple of given side's king's position
    '''
    for i, row in enumerate(state.board):
        for j, piece in enumerate(row):
            if piece // 2 == 6 and piece % 2 == turn:
                return (i, j)

    return None

# returns all possible pincer moves at a given row and col
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
            # pincer has to land at empty spot, break if tile is not empty
            if state.board[new_row][new_col] != 0:
                break
            else:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(pincer_capture(new_state, (new_row, new_col)))
                k += 1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
    return moves

# returns the state after the pincer's capture
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
        possible_firendly_pos = (new_row + dire[0] * 2, new_col + dire[1] * 2)
        hasEnemy = False
        hasFirendly = False
        hasSpace = possible_firendly_pos[0] >= 0 and possible_firendly_pos[
            0] < NUM_COLS and possible_firendly_pos[1] >= 0 and possible_firendly_pos[1] < NUM_ROWS
        if hasSpace:

            possible_enemy_tile = state.board[possible_enemy_pos[0]
                                              ][possible_enemy_pos[1]]
            hasEnemy = possible_enemy_tile != 0 and possible_enemy_tile % 2 != state.whose_move

            possible_firendly_tile = state.board[possible_firendly_pos[0]
                                                 ][possible_firendly_pos[1]]
            hasFirendly = possible_firendly_tile != 0 and possible_firendly_tile % 2 == state.whose_move

        # check if there's enemy piece in between pincer and other friendly piece
        if hasEnemy and hasFirendly and hasSpace:
            state.board[possible_enemy_pos[0]][possible_enemy_pos[1]] = 0

    return state

# returns whether the king will be in check when moves to the given new position
def king_check(state, new_pos):
    neighbors = eval.get_neighbor(new_pos[0], new_pos[1])
    for neighbor in neighbors:
        tile = state.board[neighbor[0]][neighbor[1]]
        ok_to_move = True
        # king
        if tile // 2 == 6 and tile % 2 != state.whose_move:
            return False
        # withdrawer
        elif tile // 2 == 5 and tile % 2 != state.whose_move:
            return False
        # leaper, need to check whether there is empty spot 1 tile away from leaper
        elif tile // 2 == 3 and tile % 2 != state.whose_move:
            row = neighbor[0]
            if neighbor[0] > new_pos[0]:
                row = new_pos[0] - 1
            else:
                row = new_pos[0] + 1
            col = neighbor[1]
            if neighbor[1] > new_pos[1]:
                col = new_pos[1] - 1
            else:
                col = new_pos[1] + 1
            # will be in the middle of an empty tile and a leaper
            if row >= 0 and col >= 0 and row < NUM_ROWS and col < NUM_COLS and \
                    state.board[row][col] == 0:
                return False
        # coordinator, need to check whether there is another enemy's pincer 1 tile away from pincer
        elif tile // 2 == 2 and tile % 2 != state.whose_move:
            enemy_king = get_king_pos(state, 1 - state.whose_move)
            if enemy_king is not None: 
                corner = state.board[neighbor[0], enemy_king[1]]
                # if corner is a king it must be me, cuz enemy's king is enemy_king
                if corner // 2 == 6: return False
                corner = state.board[enemy_king[0], neighbor[1]]
                if corner // 2 == 6: return False
        # pincer, need to check whether there is another enemy's pincer 1 tile away from pincer
        elif tile // 2 == 1 and tile % 2 != state.whose_move:
            row = neighbor[0]
            if neighbor[0] > new_pos[0]:
                row = new_pos[0] - 1
            else:
                row = new_pos[0] + 1
            col = neighbor[1]
            if neighbor[1] > new_pos[1]:
                col = new_pos[1] - 1
            else:
                col = new_pos[1] + 1
            # will be in the middle of two enemies' pincers
            if row >= 0 and col >= 0 and row < NUM_ROWS and col < NUM_COLS and \
                    state.board[row][col] in [2, 3] and state.board[row][col] % 2 != state.whose_move:
                return False
    return ok_to_move

# returns all possible imitator moves at a given row and col
def imitator_moves(state, row, col):
    '''
    :param state: state of the board
    :param row: row index
    :param col: col index
    :return: a list of possible states of board generated by possible imitator moves
    '''
    moves = []
    imitate_obj, imitate_pos = what_to_imitate(state, row, col)
    if imitate_obj == 'king':
        moves.append(move_piece(state, (row, col), imitate_pos))
    elif imitate_obj == 'freezer':
        moves += freezer_moves(state, row, col)
    elif imitate_obj == 'withdrawer':
        dir_to_imitate = (imitate_pos[0]-row, imitate_pos[1]-col)
        dir_to_movement = (row-imitate_pos[0], col-imitate_pos[1])
        k = 1
        new_row = row + k * dir_to_movement[0]
        new_col = col + k * dir_to_movement[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                possible_capture = withdrawer_capture(
                    new_state, (row, col), dir_to_movement)
                if possible_capture != new_state:
                    moves.append(possible_capture)
                    k += 1
                    new_row = row + k * dir_to_movement[0]
                    new_col = col + k * dir_to_movement[1]
            else:
                break
        return moves

    elif imitate_obj == 'leaper':
        moves += leaper_moves(state, row, col)
    elif imitate_obj == 'coordinator':
        moves += coordinator_capture(state, (row, col))
    elif imitate_obj == 'pincer':
        moves += pincer_moves(state, row, col)
    else:
        return moves
    return moves

# returns what the imitator will imitate according to the priorities
def what_to_imitate(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    neighbors = eval.get_neighbor(row, col)
    for neighbor in neighbors:
        tile = state.board[neighbor[0]][neighbor[1]]
        # imitate King is possible
        if tile // 2 == 6 and tile % 2 != state.whose_move:
            return 'king', (neighbor[0], neighbor[1])
        # imitate freezer if possible
        elif tile // 2 == 7 and tile % 2 != state.whose_move:
            return 'freezer', (neighbor[0], neighbor[1])
        # imitate withdrawer if possible
        elif tile // 2 == 5 and tile % 2 != state.whose_move:
            return 'withdrawer', (neighbor[0], neighbor[1])
        # leaper
        elif tile // 2 == 3 and tile % 2 != state.whose_move:
            return 'leaper', (neighbor[0], neighbor[1])
        # coordinator
        elif tile // 2 == 2 and tile % 2 != state.whose_move:
            return 'coordinator', (neighbor[0], neighbor[1])
        # pincer
        elif tile // 2 == 1 and tile % 2 != state.whose_move:
            return 'pincer', (neighbor[0], neighbor[1])
    return 'empty', (0, 0)


# check whether a given cell is frozen or not
def not_frozen(board, pos):
    neighbors = eval.get_neighbor(pos[0], pos[1])
    for neighbor in neighbors:
        piece = board.board[neighbor[0]][neighbor[1]]
        # check whether the piece is a immobilizer or freezer and make sure it's not its turn now
        if piece // 2 == 7 and piece % 7 != board.whose_move:
            return False
    return True

# move a piece on the board
def move_piece(state, pre_pos, cur_pos):
    new_state = BC.BC_state(state.board, state.whose_move)
    new_state.board[cur_pos[0]][cur_pos[1]
                                ] = new_state.board[pre_pos[0]][pre_pos[1]]
    new_state.board[pre_pos[0]][pre_pos[1]] = 0
    return new_state

# alpha beta pruning to save work and time and returns the best move
def alpha_beta_pruning(current_depth, max_ply, current_state, turn, alpha, beta, start_time, time_limit):
    # global maximum_depth
    # if current_depth > maximum_depth:
    #     maximum_depth = current_depth
    global states_evaluated, retrieved, min_eval, max_eval
    # instantly return if it exceeds time limit
    if time.time() - start_time >= time_limit * 0.9:
        return current_state
    moves = valid_moves(current_state)
    best_move = BC.BC_state(current_state.board, current_state.whose_move)
    # instantly return if there's no move or reached depth
    if not moves or current_depth == max_ply:
        return current_state

    # check each valid move
    for move in moves:
        state = alpha_beta_pruning(
            current_depth + 1, max_ply, move, turn, alpha, beta, start_time, time_limit)
        eval_val = staticEval(state)
        move_value = 0
        hash_value = hash.hash_state(state)
        # Only add to table when there is new value
        print("hash value is")
        print(hash_value)
        if hash_value in hash.zobTable:
            move_value = hash.zobTable[hash_value]
            retrieved += 1
            print(retrieved)
        else:
            move_value = eval_val
            print(hash_value)
            hash.zobTable[hash_value] = move_value
            states_evaluated += 1
        min_eval = min(min_eval, move_value)
        max_eval = max(move_value, max_eval)
        if turn == 1:
            if eval_val > alpha:
                alpha = eval_val
                best_move = state
        else:
            if eval_val < beta:
                beta = eval_val
                best_move = state
        if alpha >= beta:
            times_pruned += 1
            print(times_pruned)
            return best_move

    return best_move


def makeMove(currentState, currentRemark, timelimit=10):
    start_time = time.time()
    # saved my current state as best state for now
    best = BC.BC_state(currentState.board, currentState.whose_move)
    temp = None
    cur_ply = 1
    while cur_ply < 10:
        temp = best
        best = alpha_beta_pruning(0, cur_ply, currentState, currentState.whose_move, float(
            "-inf"), float("inf"),  start_time, timelimit)
        cur_ply += 1
        end_time = time.time()
        if end_time - start_time > timelimit * 0.9:
            best = temp
            break

    # trace back on what moved
    old_pos = None
    new_pos = None
    # loop through the whole board to see what changed
    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            # if white moved
            if currentState.whose_move == 1:
                # my piece was in this cell (i, j) and now it's empty
                if currentState.board[i][j] % 2 == 1 and best.board[i][j] == 0:
                    old_pos = (i, j)
                # cell (i, j) was empty or occupied by an enemy and now my piece is there
                if currentState.board[i][j] % 2 == 0 and best.board[i][j] % 2 == 1:
                    new_pos = (i, j)
            # black moved
            else:
                # my piece was in this cell (i, j) and now it's empty
                if (currentState.board[i][j] % 2 == 0 and currentState.board[i][j] != 0) and best.board[i][j] == 0:
                    old_pos = (i, j)
                # cell (i, j) was empty or occupied by an enemy and now my piece is there
                if (currentState.board[i][j] == 0 or currentState.board[i][j] % 2 == 1) and (best.board[i][j] != 0 and best.board[i][j] % 2 == 0):
                    new_pos = (i, j)

    move = (old_pos, new_pos) if old_pos is not None else None
    print('the coordinates: ' + str(move))
    # Change who's turn
    best.whose_move = 1 - currentState.whose_move

    return [[move, best], utterance()]


# returns nick name of the agent
def nickname():
    return "Spiderman"

# returns the introduction of the agent
def introduce():
    return "I am Spiderman. I am a powerful player. I will beat you up."

# returns the static evaluation value
def staticEval(state):
    return eval.static_eval(state)


def prepare(player2Nickname):
    return "OK"

# randomly picks a remark
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
    return utterances[randint(0, 11) % 11]

# # demo use
# def demo(cur_state, max_ply=3, time_limit=10, retrieved_from_hash=0):
#     global start_time
#     start_time = time.time()

#     # initialize a new state, set it to current state for now
#     newState = BC.BC_state(cur_state.board, cur_state.whose_move)
#     best = newState
#     temp = None
#     cur_ply = 1
#     while cur_ply < max_ply:
#         temp = best
#         best = demo_search(newState, 0, cur_ply, newState.whose_move, float(
#             "-inf"), float("inf"), time_limit, retrieved_from_hash)
#         cur_ply += 1
#         end_time = time.time()
#         if end_time - start_time > time_limit * 0.90:
#             best = temp
#             break

#     # move = ((6, 4), (3, 4)) <-- what move looks like
#     old_pos = None
#     new_pos = None
#     # Checks the board to determing the position of the piece that moved
#     for i in range(8):
#         for j in range(8):
#             if newState.whose_move == 1:
#                 # Old cell has piece on my side -> New cell is empty, then this is the old position
#                 if newState.board[i][j] % 2 == 1 and best.board[i][j] == 0:
#                     old_pos = (i, j)
#                 # Old cell is empty or has opponent's piece -> New cell has piece on my side, then this is the new position
#                 if newState.board[i][j] % 2 == 0 and best.board[i][j] % 2 == 1:
#                     new_pos = (i, j)
#             else:
#                 if (newState.board[i][j] % 2 == 0 and newState.board[i][j] != 0) and best.board[i][j] == 0:
#                     old_pos = (i, j)
#                 if (newState.board[i][j] == 0 or newState.board[i][j] % 2 == 1) and (best.board[i][j] != 0 and best.board[i][j] % 2 == 0):
#                     new_pos = (i, j)

#     move = (old_pos, new_pos)
#     if old_pos is None:
#         move = None
#     #print('the coordinates: ' + str(move))

#     # Change who's turn
#     best.whose_move = 1 - cur_state.whose_move

#     end_time = time.time()
#     print('Calculation took ' + str(end_time - start_time) + ' seconds')
#     return [move, best]


# def demo_search(current_state, current_depth, max_ply, player, alpha, beta, time_lim, retrieved_from_hash):
#     global start_time, states_evaluated, times_pruned, min_eval, max_eval
#     current_time = time.time()
#     if current_time - start_time > time_lim * 0.9:
#         return current_state

#     moves = valid_moves(current_state)
#     if not moves or current_depth == max_ply:
#         return current_state

#     optimal_state = current_state
#     # For each valid move, find the best move in the next ply
#     for move in moves:
#         state = demo_search(move, current_depth + 1, max_ply,
#                             1 - player, alpha, beta, time_lim, retrieved_from_hash)
#         move_value = 0
#         hash.hash_state(state)
#         hash_value = hash.hash_state(state)
#         # Check if state has been hashed already.
#         # Add to the hash table if not with its corresponding static evaluation value.
#         table = hash.table()
#         if hash_value in table:
#             move_value = table[hash_value]
#             retrieved_from_hash += 1
#         else:
#             move_value = eval.static_eval(state)
#             table[hash_value] = move_value
#             states_evaluated += 1
#         if move_value < min_eval:
#             min_eval = move_value
#         if move_value > max_eval:
#             max_eval = move_value
#         if player == 1:
#             if move_value > alpha:
#                 alpha = move_value
#                 if current_depth == 0:
#                     optimal_state = move
#                 else:
#                     optimal_state = state
#         else:
#             if move_value < beta:
#                 beta = move_value
#                 if current_depth == 0:
#                     optimal_state = move
#                 else:
#                     optimal_state = state

#         if alpha >= beta:
#             times_pruned += 1
#             return optimal_state

#     return optimal_state


if __name__ == "__main__":
    # MAX_PLY = 5  # moves ahead to consider
    # TIME_LIMIT = 5  # Time limit to calculation in seconds
    # SIDE = 1  # Which side should make the move

    # states_evaluated = 0
    # retrieved_from_hash = 0
    # times_pruned = 0
    # min_eval = float("inf")
    # max_eval = float("-inf")

    board = BC.parse('''
c l i - k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - I w - - -
- - - - - - - -
P P - P P P P P
F - L W K I L C       ''')

    state = BC.BC_state(board, 1)

    next_move = demo(state, MAX_PLY, TIME_LIMIT, retrieved_from_hash)
    if next_move[0] is None:
        print("CAN'T MOVE!")
    else:
        print('Moves from ' +
              str(next_move[0][0]) + ' to ' + str(next_move[0][1]))

    print(next_move[1])
    print('States evaluated: ' + str(states_evaluated))
    print('Retrieved from hash table: ' + str(retrieved_from_hash))
    print('Times pruned: ' + str(times_pruned))
    print('Maximum evaluation value: ' + str(max_eval))
    print('Minimum evaluation value: ' + str(min_eval))
