'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import PLACEHOLDER_BC_module_eval as eval
import zhash as hash
import time
import random
from random import randint

TURN = 0
zobristnum = []
mySide = 1
NUM_ROWS = 8
NUM_COLS = 8
start_time = 0
# SIDE={0:'B', 1:'W'}

ALL_DIRECTION = {BC.NORTH:(-1,0), BC.SOUTH:(1,0), BC.WEST:(0, -1), BC.EAST:(0, 1), \
                 BC.NW:(-1, -1), BC.NE:(-1,1), BC.SW:(1, -1), BC.SE:(1, 1)}

def valid_moves(state):
    # print(state)
    if state is None:
        return []
    board = BC.BC_state(state.board, state.whose_move)
    # print(whose_turn)
    whose_turn = board.whose_move
    # print(whose_turn)

    moves = []
    for i, row in enumerate(board.board):
        for j, tile in enumerate(row):
            if tile != 0 and tile % 2 == whose_turn and not_frozen(board,i,j):
#                 pincer movement
                if tile // 2 == 1:
                    moves+=pincer_moves(board, i, j)
                elif tile // 2 == 2:
#                     coordiantor movement
                    moves+=coordinator_moves(board, i , j)
                elif tile // 2 == 3:
#                     leaper movement
                    moves+=leaper_moves(board, i, j)
                elif tile // 2 == 4:
                    # IMITATOR movement
                    moves+=imitator_moves(board, i, j)
                elif tile // 2 == 5:
#                     WITHDRAWER movement
                    moves+=withdrawer_moves(board,i,j)
                elif tile // 2 == 6:
#                     King movement
                    moves+=king_moves(board,i,j)
                else:
                    moves+=freezer_moves(board,i,j)
    return moves

def freezer_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves=[]
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

def king_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves=[]
    for dir_key in range(8):
        dire = ALL_DIRECTION[dir_key]
        new_row = row + dire[0]
        new_col = col + dire[1]
        # Since the king captures when it moves, we only check once
        if new_row >=0 and new_row < NUM_COLS and new_col >=0 and new_col < NUM_ROWS and (state.board[new_row][new_col] == 0 or (state.board[new_row][new_col] != 0 and state.board[new_row][new_col] % 2 != state.whose_move)):
            moves.append(move_piece(state, (row, col), (new_row, new_col)))
    return moves



def withdrawer_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves=[]
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        k=1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(withdrawer_capture(new_state, (row, col), dir))
                k+=1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else: break

    return moves

def withdrawer_capture(state, pre_pos,dir):
    '''

    :param state:
    :param pre_pos:
    :param dir:
    :return:
    '''
    oppo_dir = (-1*dir[0], dir[1]*-1)
    if oppo_dir[0]+pre_pos[0] >=0 and oppo_dir[0]+pre_pos[0] < NUM_COLS and oppo_dir[1]+pre_pos[1] >= 0 and oppo_dir[1]+pre_pos[1] < NUM_ROWS and state.board[oppo_dir[0]][oppo_dir[1]]!=0 and state.board[oppo_dir[0]][oppo_dir[1]] % 2 !=state.whose_move:
        new_state = BC.BC_state(state.board, state.whose_move)
        new_state.board[oppo_dir[0]+pre_pos[0]][oppo_dir[1]+pre_pos[1]] = 0
        return new_state
    return BC.BC_state(state.board, state.whose_move)

def leaper_moves(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    moves=[]
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        possible_capture = leaper_capture(state, (row, col), dir)
        if possible_capture != state:
            moves.append(leaper_capture(state, (row, col), dir))
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        k=1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(new_state)
                k+=1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else: break
    return moves



def leaper_capture(state, cur_pos, dir):
    '''

    :param state: state of the board
    :param cur_pos: current position of the tile
    :param dir: direction of the leap
    :return: return a modified state after capture.
    '''
    hasSpace = cur_pos[0] + 2*dir[0]>=0 and cur_pos[0] + 2 * dir[0] < NUM_COLS and cur_pos[1] + 2*dir[1]>=0 and cur_pos[1] + 2 * dir[1] < NUM_ROWS
    # hasEnemy = False
    # hasEmpty = False
    if hasSpace:
        possible_enemy_tile = state.board[cur_pos[0]+dir[0]][cur_pos[1]+dir[1]]
        hasEnemy = possible_enemy_tile != 0 and possible_enemy_tile % 2 != state.whose_move

        possible_empty_tile = state.board[cur_pos[1]+dir[1]*2][cur_pos[1]+dir[1]*2]
        hasEmpty = possible_empty_tile == 0

        if hasSpace and hasEnemy and hasEmpty:
            new_state=move_piece(state, cur_pos, (cur_pos[0]+dir[0]*2, cur_pos[1]+dir[1]*2))
            new_state.board[cur_pos[0]+dir[0]][cur_pos[1]+dir[1]]=0
            return new_state
    return BC.BC_state(state.board, state.whose_move)
    # if cur_pos[0] + 2*dir[0]>=0 and cur_pos[0] + 2 * dir[0] < NUM_COLS and cur_pos[1] + 2*dir[1]>=0 and cur_pos[1] + 2 * dir[1] < NUM_ROWS:




def coordinator_moves(state, row, col):
    '''

    :param state: state of the board
    :param row: current row index
    :param col: column index
    :return: return a list of states of coordinator possible move
    '''

    moves=[]
    for dir_key in range(8):
        dir = ALL_DIRECTION[dir_key]
        k=1
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))
                moves.append(coordinator_capture(new_state, (new_row, new_col)))
                k+=1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else: break

    return moves

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
                moves.append(pincer_capture(new_state, (new_row, new_col)))
                k+=1
                new_row = row + k * dir[0]
                new_col = col + k * dir[1]
            else: break
    return moves

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
        hasEnemy=False
        hasFirendly=False
        hasSpace = possible_firendly_pos[0] >=0 and possible_firendly_pos[0] < NUM_COLS and possible_firendly_pos[1] >=0 and possible_firendly_pos[1] <NUM_ROWS
        if hasSpace:

            possible_enemy_tile = state.board[possible_enemy_pos[0]][possible_enemy_pos[1]]
            hasEnemy = possible_enemy_tile != 0 and possible_enemy_tile % 2 != state.whose_move


            possible_firendly_tile = state.board[possible_firendly_pos[0]][possible_firendly_pos[1]]
            hasFirendly = possible_firendly_tile != 0 and possible_firendly_tile % 2 == state.whose_move

        # check if there's enemy piece in between pincer and other friendly piece
        if hasEnemy and hasFirendly and hasSpace:
            state.board[possible_enemy_pos[0]][possible_enemy_pos[1]] = 0

    return state



def imitator_moves(state, row, col):
    '''
    :param state: state of the board
    :param row: row index
    :param col: col index
    :return: a list of possible states of board generated by possible imitator moves
    '''
    moves = []
    imitate_obj, imitate_pos = what_to_imitate(state, row, col)
    if imitate_obj == 'king': moves.append(move_piece(state, (row, col), imitate_pos))
    elif imitate_obj == 'freezer': moves+=freezer_moves(state, row, col)
    elif imitate_obj == 'withdrawer':
        dir_to_imitate = (imitate_pos[0]-row,imitate_pos[1]-col)
        dir_to_movement = (row-imitate_pos[0], col-imitate_pos[1])
        k = 1
        new_row = row + k * dir_to_movement[0]
        new_col = col + k * dir_to_movement[1]
        while new_row >= 0 and new_col >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            if state.board[new_row][new_col]==0:
                new_state=move_piece(state, (row, col), (new_row, new_col))
                possible_capture = withdrawer_capture(new_state, (row, col), dir_to_movement)
                if possible_capture != new_state:
                    moves.append(possible_capture)
                    k += 1
                    new_row = row + k * dir_to_movement[0]
                    new_col = col + k * dir_to_movement[1]
                else: break
        return moves

    elif imitate_obj == 'leaper': moves+=leaper_moves(state, row, col)
    elif imitate_obj == 'coordinator': moves+=coordinator_capture(state, row, col)
    elif imitate_obj == 'pincer': moves+=pincer_moves(state, row, col)
    else:
        return moves


def what_to_imitate(state, row, col):
    '''

    :param state:
    :param row:
    :param col:
    :return:
    '''
    neighbors = eval.get_neighbor(row,col)
    for neighbor in neighbors:
        tile = state.board[neighbor[0]][neighbor[1]]
        # imitate King is possible
        if tile // 2 == 6 and tile % 2 != state.whose_move: return 'king', (neighbor[0], neighbor[1])
        # imitate freezer if possible
        elif tile // 2 == 7 and tile % 2 != state.whose_move: return 'freezer', (neighbor[0], neighbor[1])
        # imitate withdrawer if possible
        elif tile // 2 == 5 and tile % 2 != state.whose_move: return 'withdrawer', (neighbor[0], neighbor[1])
        # leaper
        elif tile // 2 == 3 and tile % 2 != state.whose_move: return 'leaper', (neighbor[0], neighbor[1])
        # coordinator
        elif tile // 2 == 2 and tile % 2 != state.whose_move: return 'coordinator', (neighbor[0], neighbor[1])
        # pincer
        elif tile // 2 == 1 and tile % 2 != state.whose_move: return 'pincer', (neighbor[0], neighbor[1])
    return 'empty', (0,0)





def not_frozen(board, row, col):
    neighbors = eval.get_neighbor(row, col)
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



def alpha_beta_pruning(current_depth, max_ply, current_state, turn, alpha, beta, start_time, time_limit):
    # global maximum_depth
    # if current_depth > maximum_depth:
    #     maximum_depth = current_depth

    moves = current_state.get_moves(turn)
    best_move = current_state
    if time.time() - start_time >= time_limit * 0.9:
        return current_state
    if not moves or current_depth == max_ply:
        # state_evaluate_count += 1
        return current_state
    # state_expanded_count += 1

    for move in moves:
        state = alpha_beta_pruning(current_depth + 1, max_ply, move, turn, alpha, beta, start_time, time_limit)
        eval_val = state.static_eval()
        move_value = 0
        hash_value = hash.hash_state(state)
        # Only add to table when there is new value
        if hash_value in hash.table:
            move_value = hash.table[hash_value]
        else:
            move_value = eval_val(state)
            hash.table[hash_value] = move_value
        if turn == 1:
            if eval_val > alpha:
                alpha = eval_val
                best_move = state
        else:
            if eval_val < beta:
                beta = eval_val
                best_move = state

        if alpha >= beta:
            # cutoff_count += 1
            return best_move

    return best_move


# def makeMove(currentState, currentRemark, timelimit):
#     global TURN
#     # Compute the new state for a move.
#     # This is a placeholder that just copies the current state.
#     newState = BC.BC_state(currentState.board)

#     # Fix up whose turn it will be.
#     newState.whose_move = 1 - currentState.whose_move

#     # Construct a representation of the move that goes from the
#     # currentState to the newState.
#     # Here is a placeholder in the right format but with made-up
#     # numbers:
#     move = ((6, 4), (3, 4))

#     # Make up a new remark
#     new_utterance = utterance()
#     TURN += 1
#     return [[move, newState], new_utterance]
def makeMove(currentState, currentRemark, timelimit=10):
    global start_time
    start_time = time.time()

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board, 1 - currentState.whose_move)

    # Fix up whose turn it will be.
    # newState.whose_move = currentState.whose_move
    # newState.whose_move = 1 - currentState.whose_move
    best_state = newState
    last_best = None
    current_max_ply = 1
    while current_max_ply < 10:
        last_best = best_state
        best_state = alpha_beta_pruning(0, current_max_ply, newState, newState.whose_move, float("-inf"), float("inf"),  start_time ,timelimit)
        current_max_ply += 1
        end_time = time.perf_counter()
        if end_time - start_time > timelimit * 0.90:
            best_state = last_best
            break 

    # move = ((6, 4), (3, 4)) <-- what move looks like
    position_A = None
    position_B = None
    # Checks the board to determing the position of the piece that moved
    for i in range(8):
        for j in range(8):
            if newState.whose_move == 0:
                # Old cell has piece on my side -> New cell is empty, then this is the old position 
                if newState.board[i][j] % 2 == 1 and best_state.board[i][j] == 0:
                    position_A = (i, j)
                # Old cell is empty or has opponent's piece -> New cell has piece on my side, then this is the new position
                if newState.board[i][j] % 2 == 0 and best_state.board[i][j] % 2 == 1:
                    position_B = (i, j)
            else:
                if (newState.board[i][j] % 2 == 0 and newState.board[i][j] != 0) and best_state.board[i][j] == 0:
                    position_A = (i, j)
                if (newState.board[i][j] == 0 or newState.board[i][j] % 2 == 1) and (best_state.board[i][j] != 0 and best_state.board[i][j] % 2 == 0):
                    position_B = (i, j)
    
    move = (position_A, position_B)
    if position_A is None:
        move = None
    print('the coordinates: ' + str(move))

    # Change who's turn
    best_state.whose_move = 1 - currentState.whose_move

    # Make up a new remark
    newRemark = utterance()

    return [[move, best_state], newRemark]

def nickname():
    return "Spiderman"


def introduce():
    return "I am Spiderman. I am a powerful player. I will beat you up."


def staticEval(state):
    print(state)
    return eval.static_eval(state, SIDE)


def prepare(player2Nickname):
    # global mySide, P, zobristnum
    # mySide = mySide
    hash.init_table()
    return "OK"

# change all the EMPTY values back to zero
# all, changes whose turn it is so the board is ready to be returned
def revert_empty(state):
    for i, row in enumerate(state.board):
        for j, tile in enumerate(row):
            if tile // 2 == 0:
                state.board[i][j] = 0
    state.whose_move = 1 - state.whose_move


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

# demo use
def demo(currentState, max_ply=3, hash=True, time_limit=10):
    global start_time
    start_time = time.time()

    # Compute the new state for a move.
    # This is a placeholder that just copies the current state.
    newState = BC.BC_state(currentState.board, currentState.whose_move)
    # print(newState)
    # Fix up whose turn it will be.
    # newState.whose_move = currentState.whose_move
    # newState.whose_move = 1 - currentState.whose_move
    best_state = newState
    last_best = None
    current_max_ply = 1
    while current_max_ply < max_ply:
        last_best = best_state
        # print(newState.whose_move)
        best_state = demo_search(newState, 0, current_max_ply, newState.whose_move, float("-inf"), float("inf"), time_limit)
        # print(newState)
        current_max_ply += 1
        end_time = time.time()
        if end_time - start_time > time_limit * 0.90:
            best_state = last_best
            break 

    # move = ((6, 4), (3, 4)) <-- what move looks like
    position_A = None
    position_B = None
    # Checks the board to determing the position of the piece that moved
    for i in range(8):
        for j in range(8):
            if newState.whose_move == 1:
                # Old cell has piece on my side -> New cell is empty, then this is the old position 
                if newState.board[i][j] % 2 == 1 and best_state.board[i][j] == 0:
                    position_A = (i, j)
                # Old cell is empty or has opponent's piece -> New cell has piece on my side, then this is the new position
                if newState.board[i][j] % 2 == 0 and best_state.board[i][j] % 2 == 1:
                    position_B = (i, j)
            else:
                if (newState.board[i][j] % 2 == 0 and newState.board[i][j] != 0) and best_state.board[i][j] == 0:
                    position_A = (i, j)
                if (newState.board[i][j] == 0 or newState.board[i][j] % 2 == 1) and (best_state.board[i][j] != 0 and best_state.board[i][j] % 2 == 0):
                    position_B = (i, j)
    
    move = (position_A, position_B)
    if position_A is None:
        move = None
    #print('the coordinates: ' + str(move))

    # Change who's turn
    best_state.whose_move = 1 - currentState.whose_move
    # print(best_state)
    # Make up a new remark
    newRemark = "I'll think harder in some future game. Here's my move"

    end_time = time.time()
    print('Calculation took ' + str(end_time - start_time) + ' seconds')
    return [move, best_state]

def demo_search(current_state, current_depth, max_ply, player, alpha, beta, time_lim):
    global start_time, ZOBRIST_HASHING, states_evaluated, times_pruned, min_eval, max_eval, retrieved_from_hash
    current_time = time.time()
    if current_time - start_time > time_lim * 0.9:
        return current_state
    # print(current_state)

    moves = valid_moves(current_state)
    # print(moves)
    if not moves or current_depth == max_ply:
        return current_state

    optimal_state = current_state
    # For each valid move, find the best move in the next ply
    for move in moves:
        # print(move)
        state = demo_search(move, current_depth + 1, max_ply, 1 - player, alpha, beta, time_lim)
        move_value = 0
        # hash_value = hash.hash_state(state)
        # # Check if state has been hashed already.  Add to the hash table if not with its corresponding static evaluation value.
        # if ZOBRIST_HASHING and hash_value in hash.table:
        #     move_value = hash.table[hash_value]
        #     retrieved_from_hash += 1
        # else:
        # move_value = eval.static_eval(state)
        # move_value=random.randint(-100, 100)
        move_value=eval.static_eval(state)
        print(move_value)
        #     hash.table[hash_value] = move_value
        #     states_evaluated += 1
        if move_value < min_eval:
            min_eval = move_value
        if move_value > max_eval:
            max_eval = move_value
        if player == 1:
            if move_value > alpha:
                alpha = move_value
                if current_depth == 0:
                    optimal_state = move
                else:
                    optimal_state = state
        else:
            if move_value < beta:
                beta = move_value
                if current_depth == 0:
                    optimal_state = move
                else:
                    optimal_state = state
        
        if alpha >= beta:
            times_pruned += 1
            return optimal_state

    a = 5
    return optimal_state
    

if __name__ == "__main__":
    MAX_PLY = 5 # How many moves ahead to consider
    ZOBRIST_HASHING = True # Use zobrist hashing if true
    TIME_LIMIT = 10 # Time limit to calculation in seconds
    SIDE = 1 # Which side should make the move

    states_evaluated = 0
    retrieved_from_hash = 0
    times_pruned = 0
    min_eval = float("inf")
    max_eval = float("-inf")

    # Edit the board to see the best next move!
    board = BC.parse('''
c l i - k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - I w - - -
- - - - - - - -
P P - P P P P P
F - L W K I L C       ''')
    # print(board)
    # state = BC.BC_state()

    state = BC.BC_state(board, 1)

    # zh.init_table()
    # print(state.board)
    next_move = demo(state, MAX_PLY, ZOBRIST_HASHING, TIME_LIMIT)
    if next_move[0] is None:
        print("CAN'T MOVE!")
    else:
        print('Moves from ' + str(next_move[0][0]) + ' to ' + str(next_move[0][1]))
    
    print(next_move[1])
    print('States evaluated: ' + str(states_evaluated))
    # print('Retrieved from hash table: ' + str(retrieved_from_hash))
    print('Times pruned: ' + str(times_pruned))
    print('Maximum evaluation value: ' + str(max_eval))
    print('Minimum evaluation value: ' + str(min_eval))