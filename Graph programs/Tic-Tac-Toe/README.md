🧠 Tic-Tac-Toe AI (Minimax + Alpha–Beta Pruning)

A console-based Tic-Tac-Toe engine with optimal AI and full JUDGE-mode support.

📌 Project Overview

This project implements a complete Tic-Tac-Toe (Noughts and Crosses) engine in C++, featuring:

✔ Human vs. AI gameplay (GAME mode)

✔ Automated testing / evaluation mode (JUDGE mode)

✔ Fully optimal AI using Minimax with Alpha–Beta Pruning

✔ Clean ASCII board rendering

✔ Correct terminal state detection (win / loss / draw)

✔ Compatible with judge testing tools (judge run, judge run --bench, etc.)

The AI always plays perfectly and never loses.

🎮 GAME Mode — Human vs. AI

Start the program and enter:

GAME


The engine asks:

who moves first,

which symbol the human uses (X or O).

The human and the AI then alternate moves.
The AI uses Minimax + Alpha–Beta pruning to guarantee optimal play.

Example:

GAME
FIRST X
HUMAN O
1 1
AI plays...
+---+---+---+
| O | _ | _ |
+---+---+---+
| _ | X | _ |
+---+---+---+
| _ | _ | _ |
+---+---+---+

🏁 JUDGE Mode — Automated Input/Output Mode

Used for testing and evaluation (e.g., via judge run).

Input format:
JUDGE
TURN X
+---+---+---+
| _ | O | X |
+---+---+---+
| _ | _ | _ |
+---+---+---+
| _ | X | _ |
+---+---+---+


Where:

TURN X means X is the player to move.

The board is always provided as 7 lines in a fixed ASCII format.

Output:

If the position is terminal (win/loss/draw):

-1


Otherwise, print the optimal move for the player to move (row and column, 1-based):

2 2


Perfect for judge systems and automated correctness checks.

🧮 AI Engine: Minimax with Alpha–Beta Pruning

The project uses a classic minimax algorithm enhanced with alpha–beta pruning, which:

drastically reduces the number of evaluated game states,

makes the AI fast even in worst-case scenarios,

preserves optimal play (results are 100% identical to full minimax).

Evaluation rules:

Win for AI (opponent) → +10 - depth

Win for human (player) → -10 + depth

Draw → 0

Using depth encourages faster wins and slower losses.



⚙️ Build & Run
Compile (g++, MinGW, Linux, etc.):
g++ -O2 -std=c++17 main.cpp -o Tic-Tac-Toe.exe

Run GAME mode:
Tic-Tac-Toe.exe
GAME

Run JUDGE mode:
Tic-Tac-Toe.exe
JUDGE
TURN X
...

🧪 Example Bench Test (judge)
judge run --bench Tic-Tac-Toe.exe


Example result:

tic-tac-toe  t01   OK
tic-tac-toe  t02   OK
tic-tac-toe  t03   OK
...
tic-tac-toe  t07h  OK


All tests passed successfully — the AI behaves exactly as expected.

🏆 Summary

This project demonstrates:

a clean and efficient Minimax + Alpha–Beta implementation,

a fully optimal Tic-Tac-Toe AI,

a robust judge-compatible I/O interface,

an educational yet production-quality architecture.