from .minimax import check_winner

def alphabeta(board, depth, alpha, beta, is_maximizing, explored_count):
    """
    Minimax search with Alpha-Beta Pruning.
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
                    score, _ = alphabeta(board, depth + 1, alpha, beta, False, explored_count)
                    board[r][c] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    board[r][c] = 'O'
                    score, _ = alphabeta(board, depth + 1, alpha, beta, True, explored_count)
                    board[r][c] = ''
                    if score < best_score:
                        best_score = score
                        best_move = (r, c)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return best_score, best_move

def get_best_move(board):
    """
    Finds the best move for 'X' using Alpha-Beta Pruning.
    Returns: (best_move, best_score, states_explored, move_evaluations)
    """
    explored_count = [0]
    move_evaluations = {}
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    # We do a top-level manual loop to compile evaluations for all valid spots
    for r in range(3):
        for c in range(3):
            if board[r][c] == '':
                board[r][c] = 'X'
                score, _ = alphabeta(board, 1, alpha, beta, False, explored_count)
                board[r][c] = ''
                move_evaluations[(r, c)] = score
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                alpha = max(alpha, best_score)
                    
    if best_move is None:
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    best_move = (r, c)
                    break
            if best_move:
                break
                
    return best_move, best_score, explored_count[0], move_evaluations