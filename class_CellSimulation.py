import numpy as np
import os
from collections import deque
import time

class CellSimulation:
    def __init__(self, grid_size=30, time_steps=500, death_rate=0.5, percent_a=0.3, plot_steps=False, clump_size_A=10, num_clumps_A=4, repop="majority"):
        if not 0 <= death_rate <= 1 or not 0 <= percent_a <= 1:
            raise ValueError("death_rate and percent_a must be between 0 and 1")
        if grid_size <= 0 or time_steps <= 0:
            raise ValueError("grid_size and time_steps must be positive")
        
        
        self.grid_size = grid_size
        self.time_steps = time_steps
        self.death_rate = death_rate
        self.percent_a = percent_a
        self.percent_c = 1 - percent_a
        self.plot_steps = plot_steps
        self._clump_size_A = clump_size_A
        self._num_clumps_A = num_clumps_A

        #majority is just majority winner"
        #random is random
        #greater_than_1 checks if greater than 2 (for pent, hex, oct)
        #greater_than_2 checks if greater than 2 (for pent, hex, oct)
        #greater_than_3 (for oct)
        self.repop = repop

        self.directions = self.get_directions()
        
        # INITIALIZE 
        self.grid = np.random.choice(["A", "C"], size=(grid_size, grid_size), p=[percent_a, self.percent_c])

    def get_directions(self):
        return []  # Overridden in subclasses

    def add_clumps(self):
        def get_neighbors(i, j):
            neighbors = []
            for di, dj in self.directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.grid_size and 0 <= nj < self.grid_size:
                    neighbors.append((ni, nj))
            return neighbors

        cell_type = "A"
        for _ in range(self._num_clumps_A):
            # Ensure we find a suitable starting point
            attempts = 0
            while attempts < 100:
                start_i = np.random.randint(0, self.grid_size)
                start_j = np.random.randint(0, self.grid_size)

                # Check if the starting point is not already part of a clump
                if self.grid[start_i, start_j] != cell_type:
                    queue = deque([(start_i, start_j)])
                    visited = set(queue)
                    self.grid[start_i, start_j] = cell_type

                    while queue and len(visited) < self._clump_size_A:
                        i, j = queue.popleft()

                        for ni, nj in get_neighbors(i, j):
                            if (ni, nj) not in visited and self.grid[ni, nj] != cell_type:
                                self.grid[ni, nj] = cell_type
                                visited.add((ni, nj))
                                queue.append((ni, nj))
                    
                    # Successfully created a clump
                    break
            
                attempts += 1
    


    def plot_grid(self, grid, t, output_folder):
        pass  # Implement in subclasses

    def count_cells(self):
        counts = {
            "A": int(np.sum(self.grid == "A")),
            "B": int(np.sum(self.grid == "B")),
            "C": int(np.sum(self.grid == "C"))
        }
        return counts

    def kill_cells(self):
        a_c_indices = [
            (i, j) 
            for i in range(self.grid_size) 
            for j in range(self.grid_size) 
            if self.grid[i, j] in ["A", "C"]
        ]
        num_to_kill = int(self.death_rate * len(a_c_indices))
        kill_indices = np.random.choice(len(a_c_indices), size=num_to_kill, replace=False)

        for idx in kill_indices:
            i, j = a_c_indices[idx]
            self.grid[i, j] = "B"

    def repopulate_cells(self):            
        new_grid = self.grid.copy()

        def majority(count_a, count_c, i , j):
            if count_a > count_c:
                new_grid[i, j] = "A"

            elif count_c > count_a:
                new_grid[i, j] = "C"

            else:
                new_grid[i, j] = np.random.choice(["A", "C"])
    
        def random(i , j):
            new_grid[i, j] = np.random.choice(["A", "C"])
        
        def greater_than(count_a, i , j, num):
            if count_a > num:
                new_grid[i, j] = "A"

            else:
                new_grid[i, j] = "C"
    
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i, j] == "B":
                    neighbors = [
                        self.grid[i + dx, j + dy] 
                        for dx, dy in self.directions 
                        if 0 <= i + dx < self.grid_size and 0 <= j + dy < self.grid_size
                    ]
                    count_a = neighbors.count("A")
                    count_c = neighbors.count("C")
                    
                    if self.repop == "random": random(i, j)

                    elif self.repop == "greater_than_1": greater_than(count_a, i , j, 1)

                    elif self.repop == "greater_than_2": greater_than(count_a, i , j, 2)

                    elif self.repop == "greater_than_3": greater_than(count_a, i , j, 3)

                    else: majority(count_a, count_c, i , j) 

        self.grid = new_grid

    def run_simulation(self, output_folder):
        if self.plot_steps:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_folder = f"{output_folder}_{timestamp}"
            os.makedirs(output_folder, exist_ok=True)
        
        self.add_clumps()

        for t in range(self.time_steps):
            if self.plot_steps and (t < 10 or t % 100 == 0):
                self.plot_grid(self.grid, t, output_folder)

            self.kill_cells()
            self.repopulate_cells()

        if self.plot_steps:
            self.plot_grid(self.grid, self.time_steps, output_folder)



