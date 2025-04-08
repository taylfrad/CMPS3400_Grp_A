#Version: v0.1
#Date Last Updated: 2025-04-07

# Follow the coding standards listed in coding_standards.pdf 

#%% MODULE BEGINS
module_name_gl = 'data_ingestion'

'''
Version: v0.1

Description:
    Module for reading and validating air quality data from a CSV file.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    Provides a function to load data using pandas and logs reading events.
Notes:
    Ensure error handling is robust for file input.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd
import logging

#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def read_air_quality_data(file_path):
    """
    Reads the air quality CSV file.
    
    INPUT:
        file_path (str): Path to the CSV file.
    
    OUTPUT:
        DataFrame: Pandas DataFrame with the air quality data, or None if error.
    """
    try:
        data = pd.read_csv(file_path)
        logging.info("Data successfully read from %s", file_path)
        return data
    except Exception as e:
        logging.error("Error reading CSV file: %s", e)
        return None

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    # Test the function (adjust the path as necessary)
    data = read_air_quality_data("./Input/air_quality_data.csv")
    if data is not None:
        print("Data loaded successfully.")
    else:
        print("Data loading failed.")
