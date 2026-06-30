def check_winner(board):
    """
    Checks the status of the board.
    Returns:
    - 'X' if X wins
    - 'O' if O wins
    - 'Draw' if it's a tie
    - None if the game is still active
    """
    # Rows
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] and board[r][0] != '':
            return board[r][0]
    # Columns
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] and board[0][c] != '':
            return board[0][c]
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]
    # Check for empty cells
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                return None
    return 'Draw'

def minimax(board, depth, is_maximizing, explored_count):
    """
    Standard Minimax algorithm.
    Maximizer is 'X' (AI), Minimizer is 'O' (Player).
    """
    explored_count[0] += 1
    winner = check_winner(board)
    if winner == 'X':
        return 10 - depth, None
    elif winner == 'O':
        return depth - 10, None
    elif winner == 'Draw':
        return 0, None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    board[r][c] = 'X'
                    score, _ = minimax(board, depth + 1, False, explored_count)
                    board[r][c] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    board[r][c] = 'O'
                    score, _ = minimax(board, depth + 1, True, explored_count)
                    board[r][c] = ''
                    if score < best_score:
                        best_score = score
                        best_move = (r, c)
        return best_score, best_move

def get_best_move(board):
    """
    Finds the best move for 'X' using standard Minimax.
    Returns: (best_move, best_score, states_explored, move_evaluations)
    """
    explored_count = [0]
    move_evaluations = {}
    best_score = float('-inf')
    best_move = None
    
    # We do a top-level manual loop to compile evaluations for all valid spots
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'X'
                score, _ = minimax(board, 1, False, explored_count)
                board[r][c] = ''
                move_evaluations[(r, c)] = score
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                    
    # If board is full or no move found (should not happen unless game is over)
    if best_move is None:
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    best_move = (r, c)
                    break
            if best_move:
                break
                
    return best_move, best_score, explored_count[0], move_evaluations
