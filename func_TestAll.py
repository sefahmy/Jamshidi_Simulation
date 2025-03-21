import itertools
import pandas as pd
from class_CellSimulation import CellSimulation
from class_HexagonSimulation import HexagonSimulation
from class_OctagonSimulation import OctagonSimulation
from class_PentagonSimulation import PentagonSimulation


def run_simulations(output_file, conditional_output_file):
    shape_classes = {"hex": HexagonSimulation, "pent": PentagonSimulation, "oct": OctagonSimulation}
    grid_sizes = [30]
    time_steps_list = [500]
    death_rates = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    percent_a_list = [0.2, 0.3, 0.4, 0.5]
    clump_sizes_A = [10, 15, 20, 25, 30]
    num_clumps_A_list = [1, 2, 3, 4]
    repop_methods = ["random", "greater_than_1", "greater_than_2", "greater_than_3", "majority"]

    param_grid = itertools.product(shape_classes.keys(), grid_sizes, time_steps_list, death_rates, percent_a_list, clump_sizes_A, num_clumps_A_list, repop_methods)
    
    results = []
    conditional_results = []
    
    for shape, grid_size, time_steps, death_rate, percent_a, clump_size_A, num_clumps_A, repop in param_grid:
        simulation = shape_classes[shape](grid_size, time_steps, death_rate, percent_a, False, clump_size_A, num_clumps_A, repop)
        initial_counts = simulation.count_cells()
        for _ in range(simulation.time_steps):
            simulation.kill_cells()
            simulation.repopulate_cells()
        final_counts = simulation.count_cells()
        
        result = {
            "shape": shape, "grid_size": grid_size, "time_steps": time_steps, "death_rate": death_rate,
            "percent_a": percent_a, "clump_size_A": clump_size_A, "num_clumps_A": num_clumps_A, "repop": repop,
            "initial_A": initial_counts["A"], "initial_C": initial_counts["C"],
            "final_A": final_counts["A"], "final_C": final_counts["C"]
        }
        
        results.append(result)
        
        # Check the condition to add to the conditional results
        if initial_counts["A"] < initial_counts["C"] and final_counts["A"] > final_counts["C"]:
            conditional_results.append(result)
    
    # Write the regular results to the output file
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    
    # Write the conditional results to the conditional output file
    if conditional_results:
        df_conditional = pd.DataFrame(conditional_results)
        df_conditional.to_excel(conditional_output_file, index=False)


run_simulations("simulation_results.xlsx", "winning_simulation_results.xlsx")
