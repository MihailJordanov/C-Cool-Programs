🐸 Frog Game — Logic Puzzle Solver in C++

This project is a C++ implementation of the classic “Frog Jump” puzzle,
where two groups of frogs must swap sides on a narrow bridge using only valid moves.
The program uses graph traversal algorithms (DFS & BFS) to explore possible states
and find the optimal sequence of moves that leads to the goal configuration.

🎮 Game Description

Imagine a bridge with frogs facing each other:

LLL_RRR


L = frogs facing right

R = frogs facing left

_ = empty space

🧩 Rules:

Each L frog can move right one step if the space is empty (L _ → _ L).

Each L frog can jump over one R frog if there’s an empty space after it (L R _ → _ R L).

Each R frog can move left one step if the space is empty (_ R → R _).

Each R frog can jump over one L frog if there’s an empty space before it (_ L R → R L _).

The goal is to swap both groups completely:

RRR_LLL

⚙️ Features

Automatic graph generation of all reachable states from the starting position.

DFS traversal to build the full state graph.

BFS traversal to compute the shortest possible solution (minimum moves).

Prints the entire sequence of moves from start to goal.

Includes theoretical comparison:

Minimal moves = n² + 2n

💡 Example Output (for n = 3)
Enter Number! How many frogs on one side?
3
Starting Bridge:
LLL_RRR

Shortest moves: 15
Formula check (n*n + 2n): 15

  0: LLL_RRR
  1: LL_LRRR
  2: LL RLR_R
  ...
 15: RRR_LLL

🧠 Concepts Demonstrated

State-space representation using strings

Recursive DFS with unordered_set for visited tracking

BFS shortest path reconstruction with parent mapping

Graph generation and traversal techniques

🛠️ Technologies Used

C++17 / C++20

STL containers: vector, unordered_map, unordered_set, queue

Built and tested in Visual Studio

🎯 Project Goal

To visualize how graph algorithms can solve combinatorial puzzles efficiently,
showing that even a simple logic game can become a great example of
state-space search, recursion, and optimal pathfinding in C++.