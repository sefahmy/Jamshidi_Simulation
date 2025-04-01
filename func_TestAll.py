import itertools
import pandas as pd
import time
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

    # Calculate total number of simulations
    total_sims = len(shape_classes) * len(grid_sizes) * len(time_steps_list) * \
                 len(death_rates) * len(percent_a_list) * len(clump_sizes_A) * \
                 len(num_clumps_A_list) * len(repop_methods)
    
    param_grid = itertools.product(shape_classes.keys(), grid_sizes, time_steps_list, death_rates, percent_a_list, clump_sizes_A, num_clumps_A_list, repop_methods)
    
    results = []
    conditional_results = []
    start_time = time.time()
    current_sim = 0
    
    print("\nStarting simulations...\n")
    for shape, grid_size, time_steps, death_rate, percent_a, clump_size_A, num_clumps_A, repop in param_grid:
        current_sim += 1
        elapsed_time = time.time() - start_time
        avg_time_per_sim = elapsed_time / current_sim
        estimated_time_remaining = avg_time_per_sim * (total_sims - current_sim)
        
        status = (
            f"\rSimulation {current_sim}/{total_sims} ({(current_sim/total_sims*100):.1f}%) | "
            f"Current: {shape}, d={death_rate}, a={percent_a}, cs={clump_size_A}, nc={num_clumps_A}, {repop} | "
            f"Elapsed: {elapsed_time/60:.1f}m | "
            f"Remaining: {estimated_time_remaining/60:.1f}m | "
            f"Step: 0/{time_steps} | "
            f"Wins: {len(conditional_results)}"
        )
        print(status, end="", flush=True)
        
        simulation = shape_classes[shape](grid_size, time_steps, death_rate, percent_a, False, clump_size_A, num_clumps_A, repop)
        initial_counts = simulation.count_cells()
        
        for step in range(simulation.time_steps):
            if step % 100 == 0:
                print(f"\r{status[:-len(str(time_steps))-len(str(len(conditional_results)))-8]}{step}/{time_steps} | Wins: {len(conditional_results)}", end="", flush=True)
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
        
        if initial_counts["A"] < initial_counts["C"] and final_counts["A"] > final_counts["C"]:
            conditional_results.append(result)
    
    print(f"\n\nCompleted all {total_sims} simulations in {(time.time() - start_time)/60:.1f} minutes")
    print(f"Found {len(conditional_results)} winning conditions")
    
    # Write the regular results to the output file
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    
    # Write the conditional results to the conditional output file
    if conditional_results:
        df_conditional = pd.DataFrame(conditional_results)
        df_conditional.to_excel(conditional_output_file, index=False)

run_simulations("simulation_results.xlsx", "winning_simulation_results.xlsx")

#for testing 
# OctagonSimulation(grid_size= 30, time_steps= 1, plot_steps=True).run_simulation("cell_simulation_A_vs_C_clumps")

