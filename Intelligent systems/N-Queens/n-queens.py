import random

MAX_N = 51


def generate_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]


def check_is_possible(n):
    if n in (2, 3):
        #print(f"Not possible with n = {n}")
        return False
    return True


def print_pos(board):
    print(" ".join(map(str, board)))


def print_board(board):
    n = len(board)
    if n >= MAX_N:
        print(f"Board too large to display ({n}x{n})")
        return

    for row in range(n):
        line = []
        for col in range(n):
            line.append("*" if board[col] == row else "_")
        print(" ".join(line))


def conflicts_for(board, row, col):
    n = len(board)
    conflicts = 0
    for r in range(n):
        if r == row:
            continue

        c = board[r]

        if c == col:
            conflicts += 1
            continue

        if abs(r - row) == abs(c - col):
            conflicts += 1

    return conflicts


def collect_conflicted_rows(board):
    conflicted_rows = []  

    for row in range(len(board)):
        conflicts = conflicts_for(board, row, board[row])

        if conflicts > 0:
            conflicted_rows.append(row)

    return conflicted_rows


def pick_best_col_random_tiebreak(costs):

    best = min(costs)
    best_cols = []
    for i in range(len(costs)):
        if costs[i] == best:
            best_cols.append(i)
    return random.choice(best_cols)


def min_conflicts(board, max_steps=50000):
    n = len(board)
    if n == 0:
        return True

    for step in range(max_steps):
        conflicted_rows = collect_conflicted_rows(board)
        if not conflicted_rows:
            return True  

        row = random.choice(conflicted_rows)

        costs = [conflicts_for(board, row, col) for col in range(n)]

        best_col = pick_best_col_random_tiebreak(costs)

        board[row] = best_col

    return False  


def print_final(board):
    n = len(board)
    if not check_is_possible(n):
        return

    board[:] = generate_board(n)

    print("\nFirst Positions:")
    print_pos(board)

    print("\nFirst board:")
    print_board(board)

    solved = min_conflicts(board)

    if solved:
        print("\n\nFinal Positions (After Min-Conflicts):")
        print_pos(board)
        print("\nFinal board (After Min-Conflicts):")
        print_board(board)
    else:
        print("\nFailed to find solution after max steps.")

def print_final_for_test(board):
    n = len(board)

    if not check_is_possible(n):
        print(-1)
        return
    
    if n > 700:
        print(-1)
        return

    board[:] = generate_board(n)

    solved = min_conflicts(board)
    if solved:
        #print_board(board)
        print_pos(board)
    else:
        print(-1)

def main():
    n = int(input().strip())
    board = [0] * n
    print_final_for_test(board)


if __name__ == "__main__":
    main()
