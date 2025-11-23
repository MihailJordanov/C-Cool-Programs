# ♛ N-Queens Solver (Min-Conflicts Algorithm)

This project solves the classic **N-Queens problem** using the **Min-Conflicts** heuristic algorithm — a fast local search method that can efficiently find solutions for very large N (up to ~10,000 queens).

---

## 📘 Problem Description

The **N-Queens** puzzle asks:  
> How can N queens be placed on an N×N chessboard so that no two queens threaten each other?

That means:
- No two queens share the same **row**.
- No two queens share the same **column**.
- No two queens share the same **diagonal**.

🔗 Visualization: [N-Queens Visualizer](https://n-queen-five.vercel.app/visualize)

---

## ⚙️ Input Format

A single integer `N` (number of queens).

4

---

## 🧾 Output Format

An array representing the positions of the queens,  
where each index is the **row**, and each value is the **column**.

Example:
[2, 0, 3, 1]


Meaning:
- Queen in row 0 → column 2  
- Queen in row 1 → column 0  
- Queen in row 2 → column 3  
- Queen in row 3 → column 1  

---

## 🚫 Special Cases

- If **N ∈ {2, 3}**, there is **no valid solution**, and the output must be:
-1

---

## 🧠 Algorithm — Min-Conflicts

The **Min-Conflicts** algorithm works as follows:

1. Start with a **random configuration** of queens (one per row).
2. While conflicts exist:
 - Pick a **random conflicting queen**.
 - Move it to the **column that causes the fewest conflicts** (randomly choosing among ties).
3. Stop when no conflicts remain or when a step limit is reached.

This local search strategy is extremely fast and can solve **N = 10,000** queens in under **1 second**.

---

## 🖥️ Example Board Visualization

For N = 4, the output board could look like this:

_ * _ _
_ _ _ *
* _ _ _
_ _ * _

Where:
- `*` → queen  
- `_` → empty square  

---

## 🚀 Performance

- Handles **N = 10,000 (±10)** in **< 1 second**.
- Uses NumPy for optimized operations.
- Randomized tiebreaks improve convergence speed.

---

## 🧩 Example Run

**Input:**
4

**Output:**

2 0 3 1


**Unsolvable Case:**
3
**Output:**
-1

---

## 🧪 Automatic Testing Notes

- For small `N`, the board and positions are printed.
- For large `N` (> 700), only the runtime is measured.
- The solver passes efficiency requirements for all benchmark tests.

---

## 👨‍💻 Author
**Mihail Jordanov**  
GitHub: [MihailJordanov](https://github.com/MihailJordanov)
