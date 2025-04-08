#Version: v0.1
#Date Last Updated: 2025-04-07

#%% MODULE BEGINS
module_name_gl = 'config'

'''
Version: v0.1

Description:
    Contains configuration constants for the Urban Air Quality Analysis project.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    This module holds constants including file paths for input, output, and logging.
Notes:
    Ensure that file paths are specified relative to the project root.
'''

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CONFIG = {
    "input_csv": "./Input/air_quality_data.csv",  # CSV file with test data
    "output_dir": "./Output/",                     # Output folder for plots and logs
    "doc_dir": "./Doc/",                           # Documentation folder
    "log_file": "./Output/project.log"             # Log file
}

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    print("Configuration Constants:")
    print(CONFIG)
