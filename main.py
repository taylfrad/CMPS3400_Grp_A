#Version: v0.1
#Date Last Updated: 2025-04-12

#%% MODULE BEGINS
module_name_gl = 'main'

'''
Version: v0.1

Description:
    Main entry point for the Inventory Management System.
    This program reads numerical and categorical inventory data from CSV files,
    processes the data using specialized modules, generates reports, and creates visualizations.
    
Authors:
    Taylor Fradella, Angel Njoku
Date Created     :  2025-04-07
Date Last Updated:  2025-04-12

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
import os
import time
from config import CONFIG
import ui
from inventory_numeric import InventoryNumericProcessor
from inventory_categorical import InventoryCategoricalProcessor
from visualization import plot_stock_levels, plot_hazard_distribution, generate_combined_report

#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ensure output directory exists
if not os.path.exists(CONFIG['output_dir']):
    os.makedirs(CONFIG['output_dir'])

# Set up logging
logging.basicConfig(
    filename=CONFIG['log_file'], 
    level=logging.INFO, 
    format='%(asctime)s %(message)s'
)


#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def process_numeric_data(auto_visualize=False):
    """
    Process numerical inventory data.
    
    INPUT: 
        auto_visualize (bool): If True, automatically generate visualizations
    OUTPUT:
        tuple: (success, data) where success is a boolean and data is the DataFrame if successful
    """
    try:
        numeric_data = ui.load_data(CONFIG['inventory_numeric_csv'], "numeric")
        if numeric_data is None:
            return False, None
            
        numeric_processor = InventoryNumericProcessor(numeric_data)
        numeric_processor.process_and_display()
        
        # Handle visualization
        if auto_visualize or ui.get_visualization_choice():
            try:
                plot_stock_levels(numeric_data)
                ui.show_operation_status("Stock level visualization", True)
            except Exception as e:
                logging.error(f"Error generating stock visualization: {e}")
                ui.show_operation_status("Stock level visualization", False)
        
        logging.info("Numeric data processed successfully")
        return True, numeric_data
    except Exception as e:
        logging.error(f"Error processing numeric data: {e}")
        print(f"Error processing numeric data: {e}")
        return False, None
#

def process_categorical_data(auto_visualize=False):
    """
    Process categorical inventory data.
    
    INPUT: 
        auto_visualize (bool): If True, automatically generate visualizations
    OUTPUT:
        tuple: (success, data) where success is a boolean and data is the DataFrame if successful
    """
    try:
        categorical_data = ui.load_data(CONFIG['inventory_categorical_csv'], "categorical")
        if categorical_data is None:
            return False, None
            
        categorical_processor = InventoryCategoricalProcessor(categorical_data)
        categorical_processor.process_and_display()
        
        # Handle visualization
        if auto_visualize or ui.get_visualization_choice():
            try:
                plot_hazard_distribution(categorical_data)
                ui.show_operation_status("Hazard distribution visualization", True)
            except Exception as e:
                logging.error(f"Error generating hazard visualization: {e}")
                ui.show_operation_status("Hazard distribution visualization", False)
        
        logging.info("Categorical data processed successfully")
        return True, categorical_data
    except Exception as e:
        logging.error(f"Error processing categorical data: {e}")
        print(f"Error processing categorical data: {e}")
        return False, None
#

def run_all_processes():
    """
    Run all data processing, report generation, and visualizations in sequence.
    
    INPUT: None
    OUTPUT: None
    """
    ui.display_run_all_banner()
    logging.info("Run All process started")
    
    # Process numeric data
    print("\n[1/3] Processing numerical inventory data...")
    numeric_success, numeric_data = process_numeric_data(auto_visualize=True)
    
    # Process categorical data
    print("\n[2/3] Processing categorical inventory data...")
    categorical_success, categorical_data = process_categorical_data(auto_visualize=True)
    
    # Generate combined report if both data types are available
    if numeric_success and categorical_success:
        print("\n[3/3] Generating additional visualizations and summary...")
        try:
            generate_combined_report(numeric_data, categorical_data)
            ui.show_operation_status("Additional visualizations", True)
        except Exception as e:
            logging.error(f"Error generating additional visualizations: {e}")
            print(f"Error generating additional visualizations: {e}")
            ui.show_operation_status("Additional visualizations", False)
    
    # Show overall status
    print("\nProcessing Summary:")
    if numeric_success:
        ui.show_operation_status("Numerical data processing", True)
    else:
        ui.show_operation_status("Numerical data processing", False)
        
    if categorical_success:
        ui.show_operation_status("Categorical data processing", True)
    else:
        ui.show_operation_status("Categorical data processing", False)
    
    ui.display_processing_complete()
    logging.info("Run All process completed")
#

def main():
    """
    Main function that runs the Inventory Management System.
    
    INPUT: None
    OUTPUT: None
    """
    logging.info("Inventory Management System started")
    
    # Display welcome message
    ui.display_welcome_message()
    
    # Confirm file paths
    if not ui.confirm_file_paths():
        print("Program terminated by user.")
        logging.info("Program terminated by user due to missing files")
        return
    
    # Main program loop
    running = True
    while running:
        ui.display_menu()
        choice = ui.get_user_choice()
        
        if choice == 1:
            # Process numerical data
            process_numeric_data()
        elif choice == 2:
            # Process categorical data
            process_categorical_data()
        elif choice == 3:
            # Process both types of data
            print("\nProcessing both numerical and categorical data:")
            numeric_success, _ = process_numeric_data()
            categorical_success, _ = process_categorical_data()
            
            # Show overall status
            print("\nProcessing Summary:")
            ui.show_operation_status("Numerical data processing", numeric_success)
            ui.show_operation_status("Categorical data processing", categorical_success)
        elif choice == 4:
            # Run All option
            run_all_processes()
        elif choice == 5:
            # Exit program
            print("\nExiting Inventory Management System. Goodbye!")
            running = False
    
    logging.info("Inventory Management System completed successfully")
#

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    main()