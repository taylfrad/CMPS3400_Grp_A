#Version: v0.1
#Date Last Updated: 2025-04-07

# DELETE THIS comment if not needed.
# Follow the coding standards listed in coding_standards.pdf 
# Delete sections in this template if not used

#%% MODULE BEGINS
module_name_gl = 'main'

'''
Version: v0.1

Description:
    Main entry point for the Inventory Management System.
    This program reads numerical and categorical inventory data from CSV files,
    processes the data using specialized modules, generates reports, and creates visualizations.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    This module sets up configuration and logging, reads test input data,
    calls functions from the inventory numeric and categorical modules to process data,
    and generates visualizations for stock levels and hazard distribution.
Notes:
    Ensure that the Input folder contains the files:
      - inventory_numeric.csv
      - inventory_categorical.csv
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import logging
import pandas as pd
from config import CONFIG
from inventory_numeric import InventoryNumericProcessor
from inventory_categorical import InventoryCategoricalProcessor
from visualization import plot_stock_levels, plot_hazard_distribution

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No direct user interaction; this is a command-line application)

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No additional constants)

#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
logging.basicConfig(filename=CONFIG['log_file'], level=logging.INFO, format='%(asctime)s %(message)s')

#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No additional initializations)

#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No global declarations)

#%% CLASS DEFINITIONS           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (None in this file)

#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    logging.info("Inventory Management System started.")
    
    # Read numerical inventory data
    try:
        numeric_data = pd.read_csv(CONFIG['inventory_numeric_csv'])
        logging.info("Numerical inventory data read successfully.")
    except Exception as e:
        logging.error("Error reading numerical inventory data: %s", e)
        return

    # Process numerical inventory data using the child class
    numeric_processor = InventoryNumericProcessor(numeric_data)
    numeric_report = numeric_processor.generate_numeric_report()
    logging.info("Numeric Report: %s", numeric_report)
    print("Numeric Report:")
    print(numeric_report)
    
    # Generate visualization for numerical data: stock levels
    try:
        plot_stock_levels(numeric_data)
        logging.info("Stock levels visualization generated successfully.")
    except Exception as e:
        logging.error("Error generating stock levels visualization: %s", e)
    
    # Read categorical inventory data
    try:
        categorical_data = pd.read_csv(CONFIG['inventory_categorical_csv'])
        logging.info("Categorical inventory data read successfully.")
    except Exception as e:
        logging.error("Error reading categorical inventory data: %s", e)
        return

    # Process categorical inventory data using the child class
    categorical_processor = InventoryCategoricalProcessor(categorical_data)
    categorical_report = categorical_processor.generate_category_report()
    logging.info("Categorical Report: %s", categorical_report)
    print("\nCategorical Report:")
    print(categorical_report)
    
    # Generate visualization for categorical data: hazard distribution
    try:
        plot_hazard_distribution(categorical_data)
        logging.info("Hazard distribution visualization generated successfully.")
    except Exception as e:
        logging.error("Error generating hazard distribution visualization: %s", e)
    
    logging.info("Inventory Management System completed successfully.")

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    main()
