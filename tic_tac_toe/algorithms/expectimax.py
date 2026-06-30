from .minimax import check_winner

def expectimax(board, depth, is_maximizing, explored_count):
    """
    Expectimax algorithm.
    Maximizer (AI) wants to maximize score.
    Minimizer (Player) is assumed to make random moves with uniform probability.
    So at Minimizer nodes, we compute the expected value of all possible moves.
    """
    explored_count[0] += 1
    winner = check_winner(board)
    if winner == 'X':
        return 10 - depth
    elif winner == 'O':
        return depth - 10
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    board[r][c] = 'X'
                    score = expectimax(board, depth + 1, False, explored_count)
                    board[r][c] = ''
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        total_score = 0
        count = 0
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    board[r][c] = 'O'
                    score = expectimax(board, depth + 1, True, explored_count)
                    board[r][c] = ''
                    total_score += score
                    count += 1
        if count > 0:
            return total_score / count
        else:
            return 0

def get_best_move(board):
    """
    Finds the best move for 'X' using Expectimax.
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
                score = expectimax(board, 1, False, explored_count)
                board[r][c] = ''
                move_evaluations[(r, c)] = score
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                    
    if best_move is None:
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    best_move = (r, c)
                    break
            if best_move:
                break
                
    return best_move, best_score, explored_count[0], move_evaluations
