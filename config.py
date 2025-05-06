#%% MODULE BEGINS
module_name_gl = 'config'

'''
Version: v0.1
Description:
    Configuration constants for Inventory Management System.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-07
Date Last Updated: 2025-05-XX

Doc:
    Paths for input files, output directory, and log file.
'''
#%% IMPORTS
import os

#%% CONSTANTS
class Config:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        self.inventory_numeric_csv = os.path.join(project_root, "Input", "sample_data.csv")
        self.input_pickle          = os.path.join(project_root, "Input", "sample_data.pkl")
        self.output_dir            = os.path.join(project_root, "Output")
        self.doc_dir               = os.path.join(project_root, "Doc")
        self.log_file              = os.path.join(self.output_dir, "project.log")

CONFIG = Config()

#%% SELF-RUN
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.", flush=True)
    for k, v in CONFIG.__dict__.items():
        print(f"{k}: {v}", flush=True)
