#%% MODULE BEGINS
module_name_gl = 'main'

'''
Version: v0.4
Description:
    Main entry point for the Inventory Management System.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-07
Date Last Updated: 2025-05-XX

Doc:
    Orchestrates reading, processing, reporting, and visualization
    for numeric and vector inventory data.
Notes:
    Uses CONFIG for all paths; writes outputs to CONFIG.output_dir.
'''
#%% IMPORTS
import logging
import os
import pandas as pd
import numpy as np
from functools import partial

from config import CONFIG
import ui
from inventory_numeric import InventoryNumericProcessor
from inventory_vector import InventoryVector, InventoryVectorProcessor

#%% ADVANCED PYTHON DEMOS

def flexible_stats(operation, *values, round_digits=2, **options):
    """
    Demonstrates use of *args and **kwargs
    operation: 'sum', 'mean', or 'max'
    *values: any number of numeric inputs
    round_digits: how many decimals to round the result
    **options: e.g. verbose=True
    """
    if not values:
        raise ValueError("At least one value is required")
    
    # Using lambda for operation mapping
    operations = {
        'sum': lambda x: sum(x),
        'mean': lambda x: sum(x) / len(x),
        'max': lambda x: max(x)
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation!r}")
    
    result = operations[operation](values)
    
    if options.get('verbose'):
        print(f"[flexible_stats] {operation}({values}) → {result}")
    return round(result, round_digits)

def run_formula(formula_str, **vars):
    """
    Demonstrates use of eval() and **kwargs
    formula_str: e.g. "a * b + c/2"
    **vars: named variables to inject into the formula
    """
    safe_globals = {}
    try:
        return eval(formula_str, safe_globals, vars)
    except Exception as e:
        raise ValueError(f"Error evaluating {formula_str!r}: {e}")

def process_with_nonlocal():
    """
    Demonstrates use of nonlocal variables
    """
    counter = 0
    
    def increment():
        nonlocal counter
        counter += 1
        return counter
    
    return increment

#%% CONFIGURATION
os.makedirs(CONFIG.output_dir, exist_ok=True)
logging.basicConfig(
    filename=CONFIG.log_file,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

#%% FUNCTIONS

def process_numeric_data(auto_visualize=False):
    logging.info("process_numeric_data started")
    df = ui.load_data(CONFIG.inventory_numeric_csv, "numeric")
    if df is None:
        return False

    proc = InventoryNumericProcessor(df)
    proc.process_and_display()

    # Using lambda for visualization mapping
    viz_functions = {
        'histogram': lambda: proc.plot_histogram('Stock'),
        'line': lambda: proc.plot_line('ProductID', 'Stock'),
        'violin': lambda: proc.plot_violin('Stock'),
        'box': lambda: proc.plot_box('Stock'),
        'scatter': lambda: proc.plot_scatter('ProductID', 'Price')
    }

    if auto_visualize or ui.get_visualization_choice():
        try:
            for viz_name, viz_func in viz_functions.items():
                viz_func()
            ui.show_operation_status("Numeric visualizations", True)
            logging.info("Numeric visualizations saved")
        except Exception as e:
            logging.error(f"Numeric viz error: {e}")
            ui.show_operation_status("Numeric visualizations", False)

    logging.info("process_numeric_data completed")
    return True

def process_vector_data():
    logging.info("process_vector_data started")
    try:
        parent = InventoryVector.from_pickle(CONFIG.input_pickle)
    except Exception as e:
        logging.error(f"Error loading pickle: {e}")
        print(f"Error loading pickle: {e}", flush=True)
        return False

    # Using lambda for vector operations
    vector_ops = {
        'dot': lambda v1, v2: np.dot(v1, v2),
        'angle': lambda v1, v2: np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))),
        'orthogonal': lambda v1, v2: np.isclose(np.dot(v1, v2), 0)
    }

    # Probability analytics
    cols = parent._data.select_dtypes(include='number').columns
    if len(cols) >= 2:
        c1, c2 = cols[:2]
        counts = parent.joint_counts(c1, c2)
        probs = parent.joint_probabilities(c1, c2)
        ui.display_report("Joint Counts", counts.to_dict())
        ui.display_report("Joint Probabilities", probs.to_dict())
    else:
        print("Not enough numeric columns for joint analytics.", flush=True)

    # Vector operations
    if len(cols) >= 2:
        v1 = parent._data[c1].values
        v2 = parent._data[c2].values
        proc = InventoryVectorProcessor(parent._data)
        vec_ops = {
            "Dot Product": vector_ops['dot'](v1, v2),
            "Angle (deg)": np.degrees(vector_ops['angle'](v1, v2)),
            "Orthogonal?": vector_ops['orthogonal'](v1, v2)
        }
        ui.display_report("Vector Operations", vec_ops)

    # Categorical combos/perms if any string column exists
    cat_cols = parent._data.select_dtypes(include='object').columns
    if len(cat_cols) >= 1:
        cat = cat_cols[0]
        proc = InventoryVectorProcessor(parent._data)
        ui.display_report("Combinations", {cat: proc.generate_combinations(cat)})
        ui.display_report("Permutations", {cat: proc.generate_permutations(cat)})
    else:
        print("No categorical column for combos/perms.", flush=True)

    logging.info("process_vector_data completed")
    return True

def run_all_processes():
    ui.display_run_all_banner()
    logging.info("run_all_processes started")
    ok_num = process_numeric_data(auto_visualize=True)
    ok_vec = process_vector_data()
    if not ok_num:
        ui.show_operation_status("Numeric workflow", False)
    if not ok_vec:
        ui.show_operation_status("Vector workflow", False)
    ui.display_processing_complete()
    logging.info("run_all_processes completed")

def main():
    logging.info("Inventory Management System started")
    ui.display_welcome_message()

    # ── Advanced Python demos ────────────────────────────
    try:
        # Demo of *args and **kwargs
        print("→ flexible_stats demo:", flexible_stats('sum', 1, 2, 3, verbose=True), flush=True)
        
        # Demo of eval()
        print(
            "→ run_formula demo:",
            run_formula("a*b + c/2", a=4, b=3, c=10),
            flush=True
        )
        
        # Demo of nonlocal
        counter = process_with_nonlocal()
        print(f"→ nonlocal demo: {counter()}", flush=True)
        
        # Demo of lambda
        numbers = [1, 2, 3, 4, 5]
        squared = list(map(lambda x: x**2, numbers))
        print(f"→ lambda demo: {squared}", flush=True)
        
    except Exception as e:
        print(f"Advanced demo error: {e}", flush=True)
        logging.error(f"Advanced demo error: {e}")
    # ──────────────────────────────────────────────────────

    if not ui.confirm_file_paths():
        logging.info("Exited at file confirmation")
        return

    while True:
        print("\nMAIN MENU:", flush=True)
        print("1. Process Numeric Data", flush=True)
        print("2. Process Vector Data", flush=True)
        print("3. Run All", flush=True)
        print("4. Exit", flush=True)
        try:
            choice = int(input("Enter choice (1-4): "))
        except ValueError:
            continue

        if choice == 1:
            process_numeric_data()
        elif choice == 2:
            process_vector_data()
        elif choice == 3:
            run_all_processes()
        elif choice == 4:
            print("Exiting. Goodbye!", flush=True)
            logging.info("Inventory Management System exited by user")
            break

#%% SELF-RUN
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.", flush=True)
    main()
