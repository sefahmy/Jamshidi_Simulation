import os
from matplotlib import pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from class_CellSimulation import CellSimulation

class OctagonSimulation(CellSimulation):
    def get_directions(self):
        return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    #work in progress
    def plot_grid(self, grid, t, output_folder):
        # Increase figure size
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.axis('off')

        # Increase octagon size significantly
        oct_size = 1.0  # Much larger value
        spacing = 1.1 * oct_size * (1 + np.sqrt(2)/2)
        dx, dy = spacing, spacing
        
        color_map = {"A": 'yellow', "B": 'black', "C": 'cyan'}
        counts = self.count_cells()

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                x = j * dx + (i % 2) * dx/2
                y = i * dy
                cell_type = grid[i, j]
                color = color_map[cell_type]
                octagon = RegularPolygon((x, y), numVertices=8, 
                                       radius=oct_size, 
                                       orientation=np.pi/8, 
                                       color=color, 
                                       ec='k')
                ax.add_patch(octagon)

        # Set the axis limits with some padding
        padding = dx
        ax.set_xlim(-padding, grid.shape[1] * dx + padding)
        ax.set_ylim(-padding, grid.shape[0] * dy + padding)

        # Force the plot to respect the figure size
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        
        plt.title(f"Time Step: {t} | A: {counts['A']} | B: {counts['B']} | C: {counts['C']}")
        plt.savefig(os.path.join(output_folder, f"step_{t:03d}.png"), dpi=300, bbox_inches='tight')
        plt.close()

