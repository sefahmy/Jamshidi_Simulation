import os
from matplotlib import pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from class_CellSimulation import CellSimulation

class PentagonSimulation(CellSimulation):
    def get_directions(self):
        return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1)]

    #work in progress
    def plot_grid(self, grid, t, output_folder):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.axis('off')

        pent_size = 0.02
        dx, dy = 2 * pent_size * np.cos(np.pi / 5) * 1.1, 2 * pent_size * np.sin(np.pi / 5) * 1.1
        color_map = {"A": 'yellow', "B": 'black', "C": 'cyan'}

        counts = self.count_cells()

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                x, y = j * dx, i * dy
                orientation = (np.pi / 5) if (i + j) % 2 == 0 else (-np.pi / 5)  # Alternate rotations
                cell_type = grid[i, j]
                color = color_map[cell_type]
                pentagon = RegularPolygon((x, y), numVertices=5, radius=pent_size, orientation=orientation, color=color, ec='k')
                ax.add_patch(pentagon)

        plt.title(f"Time Step: {t} | A: {counts['A']} | B: {counts['B']} | C: {counts['C']}")
        plt.savefig(os.path.join(output_folder, f"step_{t:03d}.png"))
        plt.close()