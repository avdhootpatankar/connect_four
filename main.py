import math
import random

ROWS = 6
COLS = 7
PLAYER = "X"
AI = "O"
EMPTY = "."

board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board():
    for row in board:
        print(" ".join(row))
    print("0 1 2 3 4 5 6\n")


def valid_move(col):
    return board[0][col] == EMPTY


def get_row(col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def make_move(col, piece):
    row = get_row(col)
    if row is not None:
        board[row][col] = piece


def undo_move(col):
    for r in range(ROWS):
        if board[r][col] != EMPTY:
            board[r][col] = EMPTY
            break


def check_win(piece):

    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # diagonal /
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # diagonal \
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False


def board_full():
    return all(board[0][c] != EMPTY for c in range(COLS))


def evaluate():
    if check_win(AI):
        return 1000
    if check_win(PLAYER):
        return -1000
    return 0


def minimax(depth, maximizing, alpha, beta):

    score = evaluate()

    if abs(score) == 1000 or depth == 0 or board_full():
        return score

    if maximizing:

        max_eval = -math.inf

        for col in range(COLS):
            if valid_move(col):

                make_move(col, AI)
                eval = minimax(depth - 1, False, alpha, beta)
                undo_move(col)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

        return max_eval

    else:

        min_eval = math.inf

        for col in range(COLS):
            if valid_move(col):

                make_move(col, PLAYER)
                eval = minimax(depth - 1, True, alpha, beta)
                undo_move(col)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

        return min_eval


def best_move(depth):

    best_score = -math.inf
    move = random.choice([c for c in range(COLS) if valid_move(c)])

    for col in range(COLS):

        if valid_move(col):

            make_move(col, AI)
            score = minimax(depth - 1, False, -math.inf, math.inf)
            undo_move(col)

            if score > best_score:
                best_score = score
                move = col

    return move


# GAME LOOP

print("Connect 4\nYou = X, Computer = O\n")

while True:

    print_board()

    # player move
    col = int(input("Enter column (0-6): "))

    if not valid_move(col):
        print("Invalid move\n")
        continue

    make_move(col, PLAYER)

    if check_win(PLAYER):
        print_board()
        print("You win!")
        break

    if board_full():
        print("Draw")
        break

    # AI move
    print("Computer thinking...\n")

    col = best_move(4)
    make_move(col, AI)

    if check_win(AI):
        print_board()
        print("Computer wins!")
        break

    if board_full():
        print("Draw")
        break