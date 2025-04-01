import os
from matplotlib import pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from class_CellSimulation import CellSimulation

class PentagonSimulation(CellSimulation):
    def get_directions(self):
        # Define the 5 nearest neighbors
        return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1)]

    def plot_grid(self, grid, t, output_folder):
        fig, ax = plt.subplots(figsize=(20, 20))
        ax.set_aspect('equal')
        ax.axis('off')

        base_size = 0.5
        dx = 2 * base_size
        dy = 2 * base_size
        vertical_shift = base_size  # Shift odd columns up by this amount
        
        color_map = {"A": 'yellow', "B": 'black', "C": 'cyan'}
        counts = self.count_cells()

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                x = j * dx
                # Add vertical shift for odd columns
                y = i * dy + (j % 2) * vertical_shift
                
                cell_type = grid[i, j]
                color = color_map[cell_type]
                
                # Base pentagon vertices
                if j % 2 == 0:  # Even columns
                    vertices = np.array([
                        [x, y],  # bottom left
                        [x + base_size, y],  # bottom right
                        [x + 1.5 * base_size, y + base_size],  # right
                        [x + base_size, y + 2 * base_size],  # top right
                        [x, y + 2 * base_size],  # top left
                    ])
                else:  # Odd columns - flipped pentagon
                    vertices = np.array([
                        [x, y],  # bottom left
                        [x + base_size, y],  # bottom right
                        [x + base_size, y + 2 * base_size],  # top right
                        [x, y + 2 * base_size],  # top left
                        [x - 0.5 * base_size, y + base_size],  # left
                    ])
                
                pentagon = plt.Polygon(vertices, color=color, ec='k')
                ax.add_patch(pentagon)

        padding = dx
        ax.set_xlim(-padding, grid.shape[1] * dx + 2*padding)
        ax.set_ylim(-padding, grid.shape[0] * dy + vertical_shift + padding)

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        
        plt.title(f"Time Step: {t} | A: {counts['A']} | B: {counts['B']} | C: {counts['C']}")
        plt.savefig(os.path.join(output_folder, f"step_{t:03d}.png"), dpi=300, bbox_inches='tight')
        plt.close()

#for testing 
# PentagonSimulation(grid_size= 30, time_steps= 1, plot_steps=True).run_simulation("cell_simulation_A_vs_C_clumps")