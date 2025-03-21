import os
from matplotlib import pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
from class_CellSimulation import CellSimulation

class HexagonSimulation(CellSimulation):
    def get_directions(self):
        return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]

    def plot_grid(self, grid, t, output_folder):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.axis('off')

        hex_size = 0.015
        dx, dy = 3 / 2 * hex_size, np.sqrt(3) * hex_size
        color_map = {"A": 'yellow', "B": 'black', "C": 'cyan'}

        counts = self.count_cells()

        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                x, y = j * dx, i * dy + (j % 2) * dy / 2
                cell_type = grid[i, j]
                color = color_map[cell_type]
                hexagon = RegularPolygon((x, y), numVertices=6, radius=hex_size, orientation=np.pi/6, color=color, ec='k')
                ax.add_patch(hexagon)

        plt.title(f"Time Step: {t} | A: {counts['A']} | B: {counts['B']} | C: {counts['C']}")
        plt.savefig(os.path.join(output_folder, f"step_{t:03d}.png"))
        plt.close()