import collections
import heapq
import random

class Puzzle:
    """
    Represents the 8-puzzle game.
    """
    def __init__(self, initial_state):
        # The initial state of the puzzle, represented as a tuple for immutability
        # (e.g., (1, 2, 3, 4, 5, 6, 7, 8, 0) where 0 is the blank tile)
        self.initial_state = tuple(initial_state)
        # The goal state of the puzzle
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        # Dimensions of the puzzle grid (3x3 for 8-puzzle)
        self.rows = 3
        self.cols = 3

    def print_board(self, state):
        """
        Prints the puzzle board in a 3x3 grid format.
        """
        print("-" * 13)
        for i in range(self.rows):
            print("|", end=" ")
            for j in range(self.cols):
                tile = state[i * self.cols + j]
                if tile == 0:
                    print("  ", end=" | ") # Blank space
                else:
                    print(f"{tile:<2}", end=" | ")
            print()
            print("-" * 13)

    def find_blank(self, state):
        """
        Finds the index (0-8) of the blank tile (0) in the given state.
        Returns a tuple (row, col).
        """
        blank_index = state.index(0)
        return (blank_index // self.cols, blank_index % self.cols)

    def get_possible_moves(self, state):
        """
        Generates all valid next states by moving the blank tile.
        Returns a list of tuples (new_state, move_description).
        """
        blank_row, blank_col = self.find_blank(state)
        possible_moves = []

        # Define possible directions: (dr, dc, description)
        # dr: change in row, dc: change in column
        directions = [
            (-1, 0, "Up"),    # Move blank up (swap with tile above)
            (1, 0, "Down"),   # Move blank down (swap with tile below)
            (0, -1, "Left"),  # Move blank left (swap with tile to the left)
            (0, 1, "Right")   # Move blank right (swap with tile to the right)
        ]

        for dr, dc, description in directions:
            new_row, new_col = blank_row + dr, blank_col + dc

            # Check if the new position is within the grid boundaries
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                new_state_list = list(state) # Convert tuple to list for mutability
                
                # Calculate indices for swapping
                blank_idx = blank_row * self.cols + blank_col
                new_tile_idx = new_row * self.cols + new_col

                # Swap the blank tile with the tile at the new position
                new_state_list[blank_idx], new_state_list[new_tile_idx] = \
                    new_state_list[new_tile_idx], new_state_list[blank_idx]
                
                possible_moves.append((tuple(new_state_list), description))
        return possible_moves

    def is_goal(self, state):
        """
        Checks if the given state is the goal state.
        """
        return state == self.goal_state

    def is_solvable(self, state):
        """
        Checks if the given 8-puzzle state is solvable.
        An 8-puzzle is solvable if the number of inversions is even.
        The blank tile (0) is ignored for inversion count.
        """
        # Create a 1D list of tiles, excluding the blank (0)
        tiles = [tile for tile in state if tile != 0]
        inversions = 0
        n = len(tiles)

        # Count inversions
        for i in range(n):
            for j in range(i + 1, n):
                if tiles[i] > tiles[j]:
                    inversions += 1
        
        # For an 8-puzzle, it's solvable if the number of inversions is even.
        return inversions % 2 == 0

class Node:
    """
    Represents a node in the search tree.
    """
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state      # The current state of the puzzle
        self.parent = parent    # The parent node in the search path
        self.action = action    # The action (move) taken to reach this state
        self.cost = cost        # Cost from the initial state to this state (g_cost for A*)

    def get_path(self):
        """
        Reconstructs the path from the initial state to this node.
        Returns a list of (state, action) tuples.
        """
        path = []
        current = self
        while current.parent:
            path.append((current.state, current.action))
            current = current.parent
        path.append((current.state, "Initial State")) # Add the initial state
        return path[::-1] # Reverse to get path from start to goal

class Solver:
    """
    Implements various search algorithms to solve the 8-puzzle.
    """
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def bfs(self):
        """
        Solves the puzzle using Breadth-First Search (BFS).
        Explores all nodes at the current depth level before moving on to nodes at the next depth level.
        Guaranteed to find the shortest path in terms of number of moves.
        """
        if not self.puzzle.is_solvable(self.puzzle.initial_state):
            print("Puzzle is unsolvable.")
            return None, 0, 0

        start_node = Node(self.puzzle.initial_state)
        queue = collections.deque([start_node]) # Use a deque for efficient popleft
        visited = {self.puzzle.initial_state}   # Keep track of visited states to avoid cycles
        
        nodes_expanded = 0
        max_queue_size = 0

        while queue:
            max_queue_size = max(max_queue_size, len(queue))
            current_node = queue.popleft()
            nodes_expanded += 1

            if self.puzzle.is_goal(current_node.state):
                return current_node.get_path(), nodes_expanded, max_queue_size

            for new_state, action in self.puzzle.get_possible_moves(current_node.state):
                if new_state not in visited:
                    visited.add(new_state)
                    new_node = Node(new_state, current_node, action, current_node.cost + 1)
                    queue.append(new_node)
        return None, nodes_expanded, max_queue_size # No solution found

    def dfs(self):
        """
        Solves the puzzle using Depth-First Search (DFS).
        Explores as far as possible along each branch before backtracking.
        Not guaranteed to find the shortest path.
        """
        if not self.puzzle.is_solvable(self.puzzle.initial_state):
            print("Puzzle is unsolvable.")
            return None, 0, 0

        start_node = Node(self.puzzle.initial_state)
        stack = [start_node] # Use a list as a stack (LIFO)
        visited = set()      # Keep track of visited states
        
        nodes_expanded = 0
        max_stack_size = 0

        while stack:
            max_stack_size = max(max_stack_size, len(stack))
            current_node = stack.pop() # Get the last element (LIFO)
            nodes_expanded += 1

            # Avoid processing already visited states for DFS to prevent infinite loops
            # especially if the graph has cycles and we don't track path to avoid re-adding
            if current_node.state in visited:
                continue
            visited.add(current_node.state)

            if self.puzzle.is_goal(current_node.state):
                return current_node.get_path(), nodes_expanded, max_stack_size

            # Get possible moves and push them onto the stack in reverse order
            # to ensure a consistent exploration order (e.g., Right, Left, Down, Up)
            # This is not strictly necessary for correctness but helps with deterministic behavior.
            for new_state, action in reversed(self.puzzle.get_possible_moves(current_node.state)):
                if new_state not in visited:
                    new_node = Node(new_state, current_node, action, current_node.cost + 1)
                    stack.append(new_node)
        return None, nodes_expanded, max_stack_size # No solution found

    def misplaced_tiles_heuristic(self, state):
        """
        Heuristic function: Counts the number of misplaced tiles (not in their goal position).
        The blank tile (0) is not counted.
        """
        misplaced = 0
        for i in range(9):
            if state[i] != self.puzzle.goal_state[i] and state[i] != 0:
                misplaced += 1
        return misplaced

    def manhattan_distance_heuristic(self, state):
        """
        Heuristic function: Calculates the sum of Manhattan distances for each tile
        from its goal position.
        Manhattan distance = |current_row - goal_row| + |current_col - goal_col|
        The blank tile (0) is not counted.
        """
        distance = 0
        for i in range(9):
            tile = state[i]
            if tile == 0:
                continue # Ignore the blank tile

            # Get current row and column for the tile
            current_row, current_col = i // self.puzzle.cols, i % self.puzzle.cols

            # Find the goal position for this tile
            # The goal state is (1, 2, 3, 4, 5, 6, 7, 8, 0)
            # So, tile 'k' should be at index 'k-1' (if k is not 0)
            # Or, more robustly, find its index in the goal state
            goal_index = self.puzzle.goal_state.index(tile)
            goal_row, goal_col = goal_index // self.puzzle.cols, goal_index % self.puzzle.cols

            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance

    def a_star(self, heuristic_func):
        """
        Solves the puzzle using A* Search algorithm.
        Uses a heuristic function to estimate the cost from the current state to the goal.
        heuristic_func can be misplaced_tiles_heuristic or manhattan_distance_heuristic.
        """
        if not self.puzzle.is_solvable(self.puzzle.initial_state):
            print("Puzzle is unsolvable.")
            return None, 0, 0

        start_node = Node(self.puzzle.initial_state, cost=0)
        # Priority queue stores (f_cost, node_id, node)
        # node_id is used to break ties and ensure unique entries in the heap
        # since nodes might have the same f_cost but are different objects.
        # A simple counter works for node_id.
        open_set = [(heuristic_func(start_node.state), 0, start_node)]
        heapq.heapify(open_set) # Initialize as a min-heap

        # Keep track of the cheapest path to a state found so far
        g_scores = {self.puzzle.initial_state: 0}
        
        # Keep track of visited states (closed set)
        closed_set = set()

        nodes_expanded = 0
        max_open_set_size = 0
        node_counter = 0 # Unique ID for nodes in the heap

        while open_set:
            max_open_set_size = max(max_open_set_size, len(open_set))
            # Pop the node with the lowest f_cost
            f_cost, _, current_node = heapq.heappop(open_set)
            nodes_expanded += 1

            # If this state has already been processed with a lower g_score, skip it
            # This handles cases where we find a shorter path to an already expanded node
            if current_node.state in closed_set:
                continue
            
            closed_set.add(current_node.state)

            if self.puzzle.is_goal(current_node.state):
                return current_node.get_path(), nodes_expanded, max_open_set_size

            for new_state, action in self.puzzle.get_possible_moves(current_node.state):
                new_g_score = current_node.cost + 1 # Cost of moving to the new state is 1

                # If we found a shorter path to new_state or it's a new state
                if new_state not in g_scores or new_g_score < g_scores[new_state]:
                    g_scores[new_state] = new_g_score
                    new_h_score = heuristic_func(new_state)
                    new_f_score = new_g_score + new_h_score
                    
                    node_counter += 1
                    new_node = Node(new_state, current_node, action, new_g_score)
                    heapq.heappush(open_set, (new_f_score, node_counter, new_node))
        
        return None, nodes_expanded, max_open_set_size # No solution found

def get_user_input_state():
    """
    Gets the initial puzzle state from user input.
    Ensures the input is valid (9 unique numbers 0-8).
    """
    while True:
        try:
            input_str = input("Enter the initial puzzle state (9 numbers 0-8, e.g., 1 2 3 4 5 6 7 8 0): ")
            state_list = [int(x) for x in input_str.split()]

            if len(state_list) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue

            if sorted(state_list) != [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                print("Error: Please ensure numbers are 0-8 and unique.")
                continue
            
            return tuple(state_list)
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

def generate_random_solvable_state():
    """
    Generates a random, solvable 8-puzzle initial state.
    """
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    while True:
        random.shuffle(goal_state)
        temp_puzzle = Puzzle(goal_state)
        if temp_puzzle.is_solvable(tuple(goal_state)):
            return tuple(goal_state)

def main():
    """
    Main function to run the 8-puzzle game.
    """
    print("Welcome to the 8-Puzzle Solver!")
    
    initial_state = None
    while True:
        choice = input("Do you want to (1) Enter a custom initial state or (2) Generate a random solvable state? (1/2): ")
        if choice == '1':
            initial_state = get_user_input_state()
            break
        elif choice == '2':
            initial_state = generate_random_solvable_state()
            print("Generated initial state:")
            temp_puzzle = Puzzle(initial_state)
            temp_puzzle.print_board(initial_state)
            break
        else:
            print("Invalid choice. Please enter '1' or '2'.")

    puzzle = Puzzle(initial_state)
    solver = Solver(puzzle)

    if not puzzle.is_solvable(initial_state):
        print("\nThis initial puzzle state is unsolvable. Please try a different one.")
        return

    while True:
        print("\nChoose a search algorithm:")
        print("1. Breadth-First Search (BFS)")
        print("2. Depth-First Search (DFS)")
        print("3. A* Search (Misplaced Tiles Heuristic)")
        print("4. A* Search (Manhattan Distance Heuristic)")
        print("5. Exit")

        algorithm_choice = input("Enter your choice (1-5): ")

        path = None
        nodes_expanded = 0
        max_data_structure_size = 0
        algorithm_name = ""

        if algorithm_choice == '1':
            algorithm_name = "BFS"
            print(f"\nSolving with {algorithm_name}...")
            path, nodes_expanded, max_data_structure_size = solver.bfs()
        elif algorithm_choice == '2':
            algorithm_name = "DFS"
            print(f"\nSolving with {algorithm_name}...")
            path, nodes_expanded, max_data_structure_size = solver.dfs()
        elif algorithm_choice == '3':
            algorithm_name = "A* (Misplaced Tiles)"
            print(f"\nSolving with {algorithm_name}...")
            path, nodes_expanded, max_data_structure_size = solver.a_star(solver.misplaced_tiles_heuristic)
        elif algorithm_choice == '4':
            algorithm_name = "A* (Manhattan Distance)"
            print(f"\nSolving with {algorithm_name}...")
            path, nodes_expanded, max_data_structure_size = solver.a_star(solver.manhattan_distance_heuristic)
        elif algorithm_choice == '5':
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        if path:
            print(f"\nSolution found using {algorithm_name}!")
            print(f"Total moves: {len(path) - 1}") # Subtract 1 for initial state
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Maximum data structure size (queue/stack/priority queue): {max_data_structure_size}")
            print("\nSolution Path:")
            for i, (state, action) in enumerate(path):
                print(f"\nStep {i}: {action}")
                puzzle.print_board(state)
        else:
            print(f"\nNo solution found using {algorithm_name} for the given puzzle.")

if __name__ == "__main__":
    main()
