# CMPS3400_Grp_A Project Skeleton
# ==================================
# Directory Structure:
# CMPS3400_Grp_A/
# ├── Doc/
# │   ├── Report.pdf           # Final report converted from PPT
# │   ├── TaskProgressReport.xlsx
# │   └── Check_List.xlsx
# ├── Input/
# │   ├── sample_data.csv      # CSV for Parent-Child Numeric workflow
# │   └── sample_data.pkl      # Pickle for Parent-Child Vector workflow
# ├── Output/
# │   ├── *.csv                 # Exported result files (e.g., below_reorder.csv, combined_summary.csv)
# │   ├── *.png                 # Plot images (histograms, line, violin, box, scatter, hazard, etc.)
# │   └── project.log           # Log file
# ├── module_tmp.py            # Template for all modules (imports, constants, sections)
# ├── config.py                # Configuration constants and paths
# ├── main.py                  # Orchestrator script (numeric & vector workflows)
# ├── generate_test_data.py    # Utility to create sample CSV and pickle
# ├── inventory_numeric.py     # Parent1 & Child1.1: numeric data stats and plots
# ├── inventory_vector.py      # Parent2 & Child2.1: vector & probability analytics
# ├── ui.py                    # CLI interface (menus, prompts, report formatting)
# └── visualization.py         # Shared plotting functions and helpers

# Example module_tmp.py
#%% MODULE BEGINS
module_name_gl = 'module_tmp'

"""
Version: v0.x
Description:
    Generic module template for CMPS3400 final project.
Authors:
    Taylor Fradella
Date Created     : YYYY-MM-DD
Date Last Updated: YYYY-MM-DD

Doc:
    Contains standard sections for imports, constants, config, classes/functions, and main.
"""
#%% IMPORTS
import logging
# other imports...

#%% CONSTANTS
# MODULE-specific constants

#%% CONFIG
# load CONFIG if needed

#%% CLASSES / FUNCTIONS
# define classes and functions here

#%% MAIN
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # test code


# generate_test_data.py
#%% MODULE BEGINS
module_name_gl = 'generate_test_data'

"""
Version: v0.1
Description:
    Utility to create sample input files for the project.
Authors:
    Taylor Fradella
Date Created     : YYYY-MM-DD
Date Last Updated: YYYY-MM-DD

Doc:
    Generates 'sample_data.csv' and 'sample_data.pkl' in the Input/ directory with realistic test data.
"""
#%% IMPORTS
import pandas as pd
import numpy as np
import os
from config import CONFIG

#%% FUNCTIONS
def create_sample_csv(path):
    df = pd.DataFrame({
        'ProductID': np.arange(101, 111),
        'Stock': np.random.randint(0, 100, size=10),
        'Price': np.round(np.random.uniform(5, 50, size=10), 2),
        'ReorderLevel': np.random.randint(10, 50, size=10)
    })
    df.to_csv(path, index=False)
    print(f"Created sample CSV at {path}", flush=True)
    return df


def create_sample_pickle(path):
    df = pd.DataFrame({
        'A': np.random.randint(0, 10, size=10),
        'B': np.random.randint(0, 10, size=10),
        'Category': np.random.choice(['X','Y','Z'], size=10)
    })
    # Ensure previous file is closed/unlocked
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
    # Attempt to write pickle, fallback if PermissionError
    try:
        df.to_pickle(path)
    except PermissionError:
        import pickle
        with open(path, 'wb') as f:
            pickle.dump(df, f)
    print(f"Created sample pickle at {path}", flush=True)
    return df

#%% MAIN
def main():
    # Ensure the Input directory exists
    input_dir = os.path.dirname(CONFIG.inventory_numeric_csv)
    os.makedirs(input_dir, exist_ok=True)

    # Generate sample paths
    csv_path = os.path.join(input_dir, 'sample_data.csv')
    pkl_path = CONFIG.input_pickle

    # Create sample data files
    create_sample_csv(csv_path)
    create_sample_pickle(pkl_path)

if __name__ == '__main__':
    main()
