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
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.axis('off')

        oct_size = 0.02
        dx, dy = 2 * oct_size * 1.1, 2 * oct_size * 1.1
        color_map = {"A": 'yellow', "B": 'black', "C": 'cyan'}

        counts = self.count_cells()

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                x, y = j * dx, i * dy
                cell_type = grid[i, j]
                color = color_map[cell_type]
                octagon = RegularPolygon((x, y), numVertices=8, radius=oct_size, orientation=0, color=color, ec='k')
                ax.add_patch(octagon)

        plt.title(f"Time Step: {t} | A: {counts['A']} | B: {counts['B']} | C: {counts['C']}")
        plt.savefig(os.path.join(output_folder, f"step_{t:03d}.png"))
        plt.close()