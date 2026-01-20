import random

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]): return True
        if all([board[j][i] == player for j in range(3)]): return True
    if all([board[i][i] == player for i in range(3)]): return True
    if all([board[i][2 - i] == player for i in range(3)]): return True
    return False

def is_draw(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] not in ['X', 'O']]

def get_move(player, board):
    while True:
        # Show available moves
        available = [cell for row in board for cell in row if cell not in ['X', 'O']]
        print(f"Available moves: {', '.join(available)}")

        move = input(f"Player {player}, enter your move (1-9 or 'q' to quit): ").lower()

        # Allow exit anytime
        if move in ['q', 'quit', 'exit']:
            print("Game exited by player.")
            return None, None

        if not move.isdigit():
            print("Invalid input. Enter a number or 'q' to quit.")
            continue

        move = int(move)
        if move < 1 or move > 9:
            print("Invalid input. Choose a number between 1 and 9.")
            continue

        row, col = (move - 1) // 3, (move - 1) % 3
        if board[row][col] in ['X', 'O']:
            print("Cell already taken. Try again.")
            continue

        return row, col

def ai_move(board, ai_player, difficulty):
    opponent = 'O' if ai_player == 'X' else 'X'
    moves = get_available_moves(board)

    if difficulty == 'easy':
        return random.choice(moves)

    elif difficulty == 'medium':
        # Win if possible
        for r, c in moves:
            board[r][c] = ai_player
            if check_winner(board, ai_player):
                board[r][c] = str(r * 3 + c + 1)
                return r, c
            board[r][c] = str(r * 3 + c + 1)
        # Block opponent
        for r, c in moves:
            board[r][c] = opponent
            if check_winner(board, opponent):
                board[r][c] = str(r * 3 + c + 1)
                return r, c
            board[r][c] = str(r * 3 + c + 1)
        return random.choice(moves)

    elif difficulty == 'hard':
        def minimax(board, depth, is_maximizing):
            if check_winner(board, ai_player): return 10 - depth
            if check_winner(board, opponent): return depth - 10
            if is_draw(board): return 0

            if is_maximizing:
                best_score = -float('inf')
                for r, c in get_available_moves(board):
                    board[r][c] = ai_player
                    score = minimax(board, depth + 1, False)
                    board[r][c] = str(r * 3 + c + 1)
                    best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                for r, c in get_available_moves(board):
                    board[r][c] = opponent
                    score = minimax(board, depth + 1, True)
                    board[r][c] = str(r * 3 + c + 1)
                    best_score = min(score, best_score)
                return best_score

        best_move = None
        best_score = -float('inf')
        for r, c in moves:
            board[r][c] = ai_player
            score = minimax(board, 0, False)
            board[r][c] = str(r * 3 + c + 1)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

def play_game():
    scores = {"X": 0, "O": 0, "Draws": 0}
    mode = input("Choose mode: 1) PvP  2) PvAI: ")
    ai_player = None
    difficulty = None

    if mode == '2':
        ai_player = input("Choose AI player (X or O): ").upper()
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()

    # Best-of series setup
    while True:
        try:
            target = int(input("Choose target wins (3, 5, or 10): "))
            if target in [3, 5, 10]:
                break
            else:
                print("Invalid choice. Please enter 3, 5, or 10.")
        except:
            print("Invalid input. Please enter a number.")

    while True:
        board = [['1','2','3'], ['4','5','6'], ['7','8','9']]
        current_player = 'X'
        print_board(board)

        while True:
            if mode == '2' and current_player == ai_player:
                row, col = ai_move(board, ai_player, difficulty)
                chosen_cell = str(row * 3 + col + 1)
                print(f"Available moves: {', '.join([cell for row in board for cell in row if cell not in ['X','O']])}")
                print(f"AI ({ai_player}) chooses cell {chosen_cell}")
            else:
                row, col = get_move(current_player, board)
                if row is None and col is None:  # Player quit
                    return

            board[row][col] = current_player
            print_board(board)

            if check_winner(board, current_player):
                print(f"🎉 Player {current_player} wins this round!")
                scores[current_player] += 1
                break
            elif is_draw(board):
                print("🤝 It's a draw!")
                scores["Draws"] += 1
                break

            current_player = 'O' if current_player == 'X' else 'X'

        print(f"🏆 Scores: X = {scores['X']} | O = {scores['O']} | Draws = {scores['Draws']}")

        # Check if someone reached target wins
        if scores["X"] == target:
            print(f"🥇 Player X wins the series (first to {target})!")
            break
        elif scores["O"] == target:
            print(f"🥇 Player O wins the series (first to {target})!")
            break

if __name__ == "__main__":
    play_game()