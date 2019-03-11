if __name__ == "__main__":
    MAX_PLY = 4 # How many moves ahead to consider
    ZOBRIST_HASHING = True # Use zobrist hashing if true
    TIME_LIMIT = 99 # Time limit to calculation in seconds
    SIDE = WHITE # Which side should make the move

    states_evaluated = 0
    retrieved_from_hash = 0
    times_pruned = 0
    min_eval = float("inf")
    max_eval = float("-inf")

    # Edit the board to see the best next move!
    board = BC.parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C''')