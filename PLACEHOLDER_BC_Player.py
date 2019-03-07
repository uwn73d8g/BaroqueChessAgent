'''PlayerSkeletonA.py
The beginnings of an agent that might someday play Baroque Chess.

'''

import BC_state_etc as BC
import time


def static_eval(board):
    black_value=0.0
    white_value=0.0

    for r, row in enumerate(board):
        for c, col in enumerate(row):
            current_state = board
            CW = 0
            CB = 0
            rows = len(board)
            columns = len(board[0])
            for i in range(0, rows):
                for j in range(0, columns):
                    factor = 100
                    current_square = current_state[i][j]
                    if current_square != '-':
                        horizontal = [current_square]
                        diag_right = [current_square]
                        vertical = [current_square]
                        diag_left = [current_square]
                        dir = [horizontal, vertical, diag_left, diag_right]
                        for k in range(1, K):
                            horizontal += current_state[i][(j + k) % columns]  # E
                            diag_right += current_state[(i + k) % rows][(j + k) % columns]  # SE
                            vertical += current_state[(i + k) % rows][j]  # S
                            diag_left += current_state[(i + k) % rows][(j - k) % columns]  # SW

                        for k in range(K - 1, 1, -1):
                            for d in dir:
                                result = static_eval_helper(d, k)
                                if result == 0:
                                    CW += factor
                                elif result == 1:
                                    CB += factor
                                factor = factor / 10

            if mySide == 'W':
                return CW - CB * 1.5
            else:
                return CB - CW * 1.5
    return black_value - white_value


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
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]


def nickname():
    return "Newman"


def introduce():
    return "I'm Newman Barry, a newbie Baroque Chess agent."


def prepare(player2Nickname):
    pass


