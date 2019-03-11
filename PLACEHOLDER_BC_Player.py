'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import PLACEHOLDER_BC_module_eval as eval
import zhash as hash
import time
from random import randint

TURN = 0
zobristnum = []
mySide = 'W'
NUM_ROWS = 8
NUM_COLS = 8


ALL_DIRECTION = {BC.NORTH:(0,1), BC.EAST:(1,0), BC.SOUTH:(0, -1), BC.WEST:(-1, 0), BC.NW:(-1, 1), BC.NE:(1,1), BC.SW:(-1, -1), BC.SE:(1, -1)}

def valid_moves(board):
    whose_turn = board.whose_move
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
            [cur_pos[0]][king_pos[1]] = 0
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
            hasFirendly = possible_firendly_tile != 0 and possible_firendly_tile % 2 != state.whose_move

        # check if there's enemy piece in between pincer and other friendly piece
        if hasEnemy and hasFirendly and hasSpace:
            state.board[possible_enemy_pos[0]][possible_enemy_pos[1]] == 0

    return state



def imitator_moves(state, row, col):
    '''
    :param state: state of the board
    :param row: row index
    :param col: col index
    :return: a list of possible states of board generated by possible imitator moves
    '''
    moves = []
    for dir_key in range(4):
        dir = ALL_DIRECTION[dir_key]
        k = 1
        imitating = 'rest'
        moved = False
        new_row = row + k * dir[0]
        new_col = col + k * dir[1]

        while new_col >= 0 and new_row >= 0 and new_row < NUM_ROWS and new_col < NUM_COLS:
            # if the square is empty (and all squares leading up to it by the else clause)
            # then it is a valid move
            # NOTE: this could be capturing as either a leaper OR an 'other' depending on imitating
            if state.board[new_row][new_col] == 0:
                new_state = move_piece(state, (row, col), (new_row, new_col))

                moves.append(imitator_capture(new_state, (new_row, new_col), dir, imitating, k))
                k += 1

            # if its the opposite teams king, ONLY a step away, acts as a king and captures it.
            elif k == 1 and state.board[new_row][new_col] in [12, 13] and state.board[new_row][new_col] % 2 != state.whose_move: 
                moves.append(imitator_capture(new_state, (new_row, new_col), dir, 'king', k))
                break

            elif not moved and state.board[new_row][new_col] in [6,7] and state.board[new_row][new_col] % 2 != state.whose_move:
                # can jump over it        
                k += 1
                imitating = 'leaper'
                moved = True
            else:
                # square has an enemy or friendly piece. Cannot jumpy over these
                break

            new_row = row + k * dir[0]
            new_col = col + k * dir[1]


def imitator_capture(state, cur_pos, dir, imitating, k):
    '''
    check if imitator moves capture any pieces and return a new state
    :param state: state of the board
    :param cur_pos: tuple of the position
    :return: new state of after imitator captures
    '''
    new_row = cur_pos[0]+k*dir[0]
    new_col = cur_pos[1]+k*dir[1]
    captured = False
    result = []

    # imitating a king is top choice, guarantees win
    if imitating == 'king':
        new_state = move_piece(state, cur_pos, (new_row, new_col))
        revert_empty(new_state)
        result.append(new_state)
        return result

    # leaper case
    elif imitating == 'leaper':
        new_state = move_piece(state, cur_pos, (new_row, new_col))
        leaper_capture(new_state, cur_pos, dir)
        revert_empty(new_state)
        result.append(new_state)
        return result

    # withdrawer case
    elif imitating == 'rest':
        isCaptured = False
        new_state = move_piece(state, cur_pos, (new_row, new_col))
        if cur_pos[0] - dir[0] >= 0 and cur_pos[0] - dir[0] < NUM_ROWS and cur_pos[1] - dir[1]  >= 0 and \
            cur_pos[1] - dir[1] < NUM_COLS and new_state.board[cur_pos[0] - dir[0]][cur_pos[1] - dir[1]] in [10, 11] and \
                new_state.board[cur_pos[0] - dir[0]][cur_pos[1] - dir[1]] % 2 != state.whose_move:
            new_state.board[cur_pos[0] - new_row][cur_pos[1] - new_col] = 0
            isCaptured = True
        # NOTE: ONLY return if captures are made in order to prevent unnecessarily expanding state tree. i.e. dont want
        # to have a state for capturing as a withdrawer, a state for capturing as a coordinator, etc when all of them dont
        # capture anything and generate identical states.
        if isCaptured:
            revert_empty(new_state)
            result.append(new_state)

            # reset board for next possible capture type
            new_state = move_piece(state, cur_pos, (new_row, new_col))
            captured = True


        # pincher case
        isCaptured = False
        for dir_key in range(4):
            dir = ALL_DIRECTION[dir_key]

            # check whether 2 steps away is a friendly piece and whether 1 step away is an enemy
            if new_row + 2*dir[0] >= 0 and new_row + 2*dir[0] < NUM_ROWS and new_col + 2*dir[1] >= 0 and new_col + 2*dir[1]  < NUM_COLS and \
                    new_state.board[new_row][new_col] % 2 == new_state.board[new_row + 2*dir[0]][new_col + 2*dir[1]] % 2 and \
                        new_state.board[new_row][new_col] % 2 != new_state.board[new_row + dir[0]][new_col + dir[1]] % 2 and new_state.board[new_row + dir[0]][new_col + dir[1]] in [2,3]:

                new_state.board[new_row + dir[0]][new_col + dir[1]] = 0
                isCaptured = True

        if isCaptured:
            revert_empty(new_state)
            # yield new_state
            result.append(new_state)
            # reset board for next move type
            new_state = move_piece(state, cur_pos, (new_row, new_col))
            captured = True


        # take care of coordinator captures
        isCaptured = False
        for i, row in enumerate(new_state.board):
            for j, piece in enumerate(row):
                if piece in [12, 13] and piece % 2 == new_state.whose_move:
                    # find kings location
                    king_row = i
                    king_col = j

                    # if there is an enemy piece at the intersection of coordinator row and king column, capture it
                    if new_state.board[new_row][king_col] in [4,5] and new_state.board[new_row][king_col] % 2 != new_state.whose_move:
                        new_state.board[new_row][king_col] = 0
                        isCaptured = True

                    # if there is an enemy piece at the intersection of coordinator row and king column, capture it
                    if new_state.board[king_row][new_col] in [4,5] and new_state.board[king_row][new_col] % 2 != new_state.whose_move:
                        new_state.board[king_row][new_col] = 0
                        isCaptured = True

                    break

        if isCaptured:
            revert_empty(new_state)
            # yield new_state
            result.append(new_state)
            captured = True

        # if no moves result in a capture (regardless of which piece we are imitating) we still want to return
        # at least one move: the move that just changes the square of the imitator.
        if not captured:
            revert_empty(new_state)
            # yield new_state
            result.append(new_state)




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
        state = alpha_beta_pruning(current_depth + 1, max_ply, move, turn, alpha, beta, start_time,
                                    isTimed, default_move, time_limit)
        eval_val = state.static_eval()
        move_value = 0
        hash_value = hash.hash_state(state)
        # Only add to table when there is new value
        if hash_value in hash.table:
            move_value = hash.table[hash_value]
        else:
            move_value = eval_val(state)
            hash.table[hash_value] = move_value
        if turn == 'W':
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

# if __name__ == "__main__":
#     MAX_PLY = 4 # How many moves ahead to consider
#     ZOBRIST_HASHING = True # Use zobrist hashing if true
#     TIME_LIMIT = 99 # Time limit to calculation in seconds
#     SIDE = WHITE # Which side should make the move

#     states_evaluated = 0
#     retrieved_from_hash = 0
#     times_pruned = 0
#     min_eval = float("inf")
#     max_eval = float("-inf")

#     # Edit the board to see the best next move!
#     board = BC.parse('''
# c l i w k i l f
# p p p p p p p p
# - - - - - - - -
# - - - - - - - -
# - - - - - - - -
# - - - - - - - -
# P P P P P P P P
# F L I W K I L C''')
