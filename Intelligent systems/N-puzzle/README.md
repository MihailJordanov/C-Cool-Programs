# 🧩 N-Puzzle Solver (IDA* Search with Linear Conflict Heuristic)

A fast and memory-efficient solver for the **N-Puzzle** problem (e.g. 8-puzzle, 15-puzzle), implemented in Python using the **Iterative Deepening A\*** (IDA*) search algorithm combined with **Manhattan distance + Linear Conflict heuristic**.

---

## 📖 What is the N-Puzzle?

The N-Puzzle is a sliding-tile game consisting of an `m × m` grid with numbered tiles and one empty space.  
The goal is to reach a configuration where all tiles are in ascending order, and the empty space (0) is in the designated goal position.

Example (3×3):

Start: Goal:
1 2 3 1 2 3
4 0 6 4 5 6
7 5 8 7 8 0

🔗 Try it online: [N-Puzzle Game](https://appzaza.com/slide-puzzle)

## ⚙️ Algorithm Overview

### 🔍 IDA* Search
This project uses **IDA\*** — *Iterative Deepening A*** — a memory-efficient variant of A*.  
Instead of storing all visited nodes, IDA* performs a **depth-first search** with increasing cost limits (`f = g + h`).

Each iteration deepens the search threshold until a solution is found:

threshold = heuristic(start)
while True:
result = dfs(threshold)
if result == FOUND: return path
threshold = result


### 🧠 Heuristic Function

The solver uses a **combined admissible heuristic**:

\[
h = h_{Manhattan} + 2 \times \text{(# linear conflicts)}
\]

- **Manhattan Distance** — Sum of distances each tile is away from its goal position.  
- **Linear Conflict** — Adds `+2` for every pair of tiles in the same row/column that are reversed in goal order.  
  This correction maintains admissibility and gives tighter estimates.

This makes the search significantly faster than pure Manhattan.

---

## 🧮 Solvability Check

Before running IDA*, the program verifies that the input puzzle is **solvable** using inversion parity rules:

- For odd-width boards → solvable if inversion count is even.  
- For even-width boards → depends on both inversion count and the row of the blank tile.

Unsolvable puzzles are reported immediately with:
-1

---

## 🚀 Usage

### 🧩 Input Format

n
I
<rows of puzzle>

where:
- `n` – number of tiles (e.g. `8` for 3×3 puzzle, `15` for 4×4)
- `I` – index of the blank tile in the goal (use `-1` for last position)
- next `m` lines – puzzle rows (0 represents the blank)

### ✅ Example Input

8
-1
1 2 3
4 5 6
0 7 8

### 📤 Example Output

2
left
left  


If the puzzle is unsolvable:
-1


---

## 🧠 Example Run

```bash
python n_puzzel.py < input.txt
```

Output:
Number of moves
Move sequence (each on new line): left, right, up, down



⚡ Optimizations

Uses NumPy for efficient state operations

Precomputed goal positions for O(1) tile lookup

Visited-set hashing via tuple(state.flatten())

Neighbor reordering by minimal estimated cost (f = g + h)

Optional heuristic caching for repeated sub-states

These optimizations ensure performance within time limits even for 15-puzzle cases.

🧑‍💻 Author

Mihail Jordanov
GitHub: [MihailJordanov](https://github.com/MihailJordanov)

