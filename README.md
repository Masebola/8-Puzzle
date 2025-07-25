# 8-Puzzle Solver (Python)

This is a command-line Python program that solves the classic **8-puzzle game** using three different search algorithms:

- **Breadth-First Search (BFS)**
- **Depth-First Search (DFS)**
- **A\* Search Algorithm**
  - With **Misplaced Tiles Heuristic**
  - With **Manhattan Distance Heuristic**

The program allows you to choose whether to enter your own puzzle state or generate a random, solvable one.

---

## 🔧 How It Works

The 8-puzzle is a sliding puzzle consisting of a 3x3 grid with 8 numbered tiles and one blank space. The goal is to reach the following state:

1 2 3
4 5 6
7 8 [ ]

You move the blank space (represented as `0`) to rearrange the tiles.

---

## 📌 Features

- Detects whether a puzzle is **solvable** before running any algorithm
- Choose between **user-defined** or **random puzzle input**
- Shows number of moves, nodes expanded, and memory usage
- Prints the full path from the initial state to the goal

---

## ▶️ How to Run

### 1. Install Python (if not already installed)

Make sure you're using **Python 3.6 or above**.

### 2. Run the program

```bash
python puzzle_solver.py

---

3. Choose your input method

You'll be prompted to:

    Enter a custom puzzle state (e.g., 1 2 3 4 5 6 7 8 0)

    Or generate a random, solvable puzzle

4. Choose a search algorithm

Select one of the following options:

    Breadth-First Search (BFS)

    Depth-First Search (DFS)

    A* Search (Misplaced Tiles Heuristic)

    A* Search (Manhattan Distance Heuristic)

    Exit

🧠 Heuristics (for A*)

    Misplaced Tiles: Counts the number of tiles not in their goal position.

    Manhattan Distance: Calculates how far each tile is from its goal using row/column distances.


✅ Requirements

    Python 3.6+

    No external packages required (uses built-in heapq, collections, random)
```
