#Version: v0.1
#Date Last Updated: 2025-04-12

#%% MODULE BEGINS
module_name_gl = 'config'

'''
Version: v0.1

Description:
    Contains configuration constants for the Inventory Management System.
    
Authors:
    Taylor Fradella, Angel Njoku
Date Created     :  2025-04-07
Date Last Updated:  2025-04-12

Doc:
    This module holds file paths for input, output, and log file settings.
Notes:
    All paths are relative to the project root.
'''

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CONFIG = {
    "inventory_numeric_csv": "./Input/inventory_numeric.csv",   # Numerical inventory file
    "inventory_categorical_csv": "./Input/inventory_categorical.csv",   # Categorical inventory file
    "output_dir": "./Output/",                     # Output folder for reports and logs
    "doc_dir": "./Doc/",                           # Documentation folder
    "log_file": "./Output/project.log"             # Log file
}


#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    print("Configuration Constants:")
    for key, value in CONFIG.items():
        print(f"  {key}: {value}")