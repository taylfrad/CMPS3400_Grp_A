#Version: v0.1
#Date Last Updated: 2025-04-07

#%% MODULE BEGINS
module_name_gl = 'main'

'''
Version: v0.1

Description:
    Main entry point for the Urban Air Quality Analysis project.
    It orchestrates the reading, analysis, and visualization of data.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    This module initializes the program, sets up logging, and calls
    functions from the data ingestion, analysis, and visualization modules.
Notes:
    Ensure imported modules adhere to project coding standards.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import logging
from config import CONFIG
from data_ingestion import read_air_quality_data
from analysis import compute_statistics
from visualization import plot_air_quality


#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logging.basicConfig(filename=CONFIG['log_file'], level=logging.INFO, format='%(asctime)s %(message)s')


#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    logging.info("Urban Air Quality Analysis started.")
    
    # Read input data from CSV
    data = read_air_quality_data(CONFIG['input_csv'])
    if data is None:
        logging.error("Failed to read data. Exiting.")
        return
    
    # Compute statistics from the data
    stats = compute_statistics(data)
    logging.info("Data statistics computed successfully.")
    
    # Generate visualizations and save output files
    plot_air_quality(data, stats)
    logging.info("Visualization completed. Exiting program.")

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    main()
