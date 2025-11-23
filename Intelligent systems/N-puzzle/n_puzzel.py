import math
import numpy as np




def inversions_parity(state: np.ndarray) -> int:
    flat = state.flatten()
    flat = flat[flat != 0]
    inv_matrix = flat[:, None] > flat[None, :]
    inversions = np.triu(inv_matrix, k=1).sum()
    return inversions % 2


def row_from_bottom(state: np.ndarray) -> int:
    m = state.shape[0]
    r, _ = np.argwhere(state == 0)[0]
    return m - r


def is_solvable(start: np.ndarray, goal: np.ndarray) -> bool:
    m = start.shape[0]

    if m % 2 == 1:
        return inversions_parity(start) == inversions_parity(goal)
    else:
        s_parity = (inversions_parity(start) + row_from_bottom(start)) % 2
        g_parity = (inversions_parity(goal) + row_from_bottom(goal)) % 2
        return s_parity == g_parity



def build_goal(n: int, I: int):
    m = int(math.sqrt(n + 1))
    if (n + 1) // m != m:
        raise ValueError("not correct N!")

    if I == -1:
        I = n

    goal = np.zeros((m, m), dtype=int)
    cur = 1
    for idx in range(n + 1):
        r, c = divmod(idx, m)
        goal[r, c] = 0 if idx == I else cur
        if idx != I:
            cur += 1
    return goal


def heuristic_combined(state: np.ndarray, goal: np.ndarray, positions=None) -> int:
    m = state.shape[0]
    if positions is None:
        positions = {val: (r, c) for r, row in enumerate(goal) for c, val in enumerate(row)}

    # Manhattan
    manh = 0
    for r in range(m):
        for c in range(m):
            v = state[r, c]
            if v == 0:
                continue
            gr, gc = positions[v]
            manh += abs(r - gr) + abs(c - gc)

    # Linear conflicts по редове 
    conflicts = 0
    for r in range(m):
        row_vals = []
        for c in range(m):
            v = state[r, c]
            if v != 0 and positions[v][0] == r:  
                row_vals.append(positions[v][1])  

        for i in range(len(row_vals)):
            ci = row_vals[i]
            for j in range(i + 1, len(row_vals)):
                cj = row_vals[j]
                if ci > cj:
                    conflicts += 1

    # Linear conflicts по колони
    for c in range(m):
        col_vals = []
        for r in range(m):
            v = state[r, c]
            if v != 0 and positions[v][1] == c:  
                col_vals.append(positions[v][0]) 
        for i in range(len(col_vals)):
            ri = col_vals[i]
            for j in range(i + 1, len(col_vals)):
                rj = col_vals[j]
                if ri > rj:
                    conflicts += 1

    return manh + 2 * conflicts


def find_zero(state: np.ndarray):
    r, c = np.argwhere(state == 0)[0]
    return int(r), int(c)


def get_neighbors_with_moves(state: np.ndarray, last_move=None):
    m = state.shape[0]
    zr, zc = find_zero(state)

    directions = [
        (1, 0, "up"),
        (0, 1, "left"),
        (-1, 0, "down"),
        (0, -1, "right"),
    ]
    opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}

    for dr, dc, move in directions:
        # избягваме връщане назад
        if last_move and opposite[last_move] == move:
            continue
        nr, nc = zr + dr, zc + dc
        if 0 <= nr < m and 0 <= nc < m:
            new_state = state.copy()
            new_state[zr, zc], new_state[nr, nc] = new_state[nr, nc], new_state[zr, zc]
            yield new_state, move


def serialize(state: np.ndarray):
    return tuple(state.flatten())


def search(path, visited, g, threshold, goal, moves, last_move):
    node = path[-1]
    h = heuristic_combined(node, goal)
    f = g + h

    if f > threshold:
        return f
    if np.array_equal(node, goal):
        return "FOUND"

    min_cost = float("inf")
    for neighbor, move in get_neighbors_with_moves(node, last_move):
        key = serialize(neighbor)
        if key in visited:
            continue

        visited.add(key)
        path.append(neighbor)
        moves.append(move)

        temp = search(path, visited, g + 1, threshold, goal, moves, move)
        if temp == "FOUND":
            return "FOUND"
        if temp < min_cost:
            min_cost = temp

        path.pop()
        moves.pop()
        visited.remove(key)

    return min_cost


def ida_star_moves(start: np.ndarray, goal: np.ndarray):
    threshold = heuristic_combined(start, goal)
    path = [start]
    moves = []
    visited = {serialize(start)}

    while True:
        temp = search(path, visited, 0, threshold, goal, moves, last_move=None)
        if temp == "FOUND":
            return moves[:]
        if temp == float("inf"):
            return None
        threshold = temp


def print_solution_moves(moves):
    if moves is None:
        print("-1")
    else:
        print(len(moves))
        print("\n".join(moves))


def main():
    n = int(input().strip())
    I = int(input().strip())

    m = int(math.sqrt(n + 1))
    if (n + 1) // m != m:
        print("Not correct n")
        return

    

    start = np.array([list(map(int, input().split())) for _ in range(m)], dtype=int)
    goal = build_goal(n, I)


    if not is_solvable(start, goal):
        print("-1")
        return

    moves = ida_star_moves(start, goal)
    print_solution_moves(moves)


if __name__ == "__main__":
    main()
