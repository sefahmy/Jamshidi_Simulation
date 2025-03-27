import unittest
import numpy as np
import os
import shutil

from class_CellSimulation import CellSimulation
from class_HexagonSimulation import HexagonSimulation

class TestCellSimulation(unittest.TestCase):
    def setUp(self):
        # Create a test output directory
        self.test_output_dir = "test_output"
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        # Remove the test output directory after tests
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    def test_initialization(self):
        # Test basic initialization parameters
        sim = CellSimulation(grid_size=50, time_steps=100, death_rate=0.3, percent_a=0.4)
        
        self.assertEqual(sim.grid_size, 50)
        self.assertEqual(sim.time_steps, 100)
        self.assertEqual(sim.death_rate, 0.3)
        self.assertEqual(sim.percent_a, 0.4)
        self.assertEqual(sim.percent_c, 0.6)

    def test_initial_grid_distribution(self):
        # Test initial grid distribution
        sim = CellSimulation(grid_size=100, percent_a=0.3)
        
        total_cells = sim.grid_size * sim.grid_size
        a_count = np.sum(sim.grid == "A")
        c_count = np.sum(sim.grid == "C")

        # Check if distribution is close to expected
        self.assertAlmostEqual(a_count / total_cells, 0.3, delta=0.1)
        self.assertAlmostEqual(c_count / total_cells, 0.7, delta=0.1)

    def test_kill_cells(self):
        # Test cell killing mechanism
        np.random.seed(42)  # For reproducibility
        sim = CellSimulation(grid_size=30, death_rate=0.5)
        
        # Store initial state
        initial_a_c_count = np.sum((sim.grid == "A") | (sim.grid == "C"))
        
        # Kill cells
        sim.kill_cells()
        
        # Count B cells after killing
        b_count = np.sum(sim.grid == "B")
        
        # Check if approximately half of A and C cells are killed
        self.assertAlmostEqual(b_count / initial_a_c_count, 0.5, delta=0.1)

    def test_add_clumps(self):
        # Test clump addition
        sim = HexagonSimulation(grid_size=50, num_clumps_A=3, clump_size_A=20)
        
        # Store initial state
        initial_grid = sim.grid.copy()
        
        # Add clumps
        sim.add_clumps()
        
        # Check if clumps are added
        a_count_initial = np.sum(initial_grid == "A")
        a_count_after = np.sum(sim.grid == "A")
        
        self.assertGreater(a_count_after, a_count_initial)

    def test_repopulation_strategies(self):
        # Test different repopulation strategies
        strategies = ["majority", "random", "greater_than_1", "greater_than_2"]
        
        for strategy in strategies:
            sim = HexagonSimulation(grid_size=30, repop=strategy)
            
            # Force some B cells
            sim.grid[10:20, 10:20] = "B"
            
            # Store initial state
            initial_grid = sim.grid.copy()
            
            # Repopulate
            sim.repopulate_cells()
            
            # Check that B cells are replaced
            b_count_after = np.sum(sim.grid == "B")
            self.assertEqual(b_count_after, 0)

    def test_plot_grid(self):
        # Test plot grid method doesn't raise exceptions
        sim = HexagonSimulation(grid_size=30, plot_steps=True)
        
        try:
            sim.plot_grid(sim.grid, 0, self.test_output_dir)
            # Check if plot is created
            self.assertTrue(os.path.exists(os.path.join(self.test_output_dir, "step_000.png")))
        except Exception as e:
            self.fail(f"plot_grid raised {type(e).__name__} unexpectedly!")

if __name__ == '__main__':
    unittest.main()