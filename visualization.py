#Version: v0.1
#Date Last Updated: 2025-04-07

# Follow the coding standards listed in coding_standards.pdf 

#%% MODULE BEGINS
module_name_gl = 'visualization'

'''
Version: v0.1

Description:
    Module for visualizing inventory management data.
    Provides functions to generate visualizations for both the numerical
    inventory data (e.g., stock levels) and the categorical data (e.g., distribution 
    of hazard classes).
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    Functions:
      - plot_stock_levels: Creates a bar chart of stock levels by ProductID.
      - plot_hazard_distribution: Creates a bar chart for the distribution of HazardClass
        from the categorical inventory data.
Notes:
    Make sure the CONFIG['output_dir'] folder exists.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import os
from config import CONFIG

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No user interface code)

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (None)

#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (Not applicable)

#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (None)

#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No global declarations)

#%% CLASS DEFINITIONS           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No classes defined here; this module contains only visualization functions)

#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def plot_stock_levels(numeric_data):
    """
    Plots a bar chart of stock levels for each product based on the numerical inventory data.
    
    INPUT:
        numeric_data (DataFrame): Must contain columns 'ProductID' and 'Stock'.
    
    OUTPUT:
        Saves the generated plot to CONFIG['output_dir'] as 'stock_levels.png'.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(numeric_data['ProductID'], numeric_data['Stock'], color='skyblue')
    plt.xlabel("Product ID")
    plt.ylabel("Stock Level")
    plt.title("Stock Levels by Product")
    plt.tight_layout()
    output_file = os.path.join(CONFIG['output_dir'], "stock_levels.png")
    plt.savefig(output_file)
    plt.close()

def plot_hazard_distribution(categorical_data):
    """
    Plots a bar chart of the inventory items grouped by hazard class.
    
    INPUT:
        categorical_data (DataFrame): Must contain a 'HazardClass' column
            with values like 'A', 'B', 'C', or 'D'.
    
    OUTPUT:
        Saves the generated plot to CONFIG['output_dir'] as 'hazard_distribution.png'.
    """
    # Count the number of items in each hazard class
    hazard_counts = categorical_data['HazardClass'].value_counts(sort=False)
    plt.figure(figsize=(8, 6))
    hazard_counts.plot(kind='bar', color='salmon')
    plt.xlabel("Hazard Class")
    plt.ylabel("Number of Items")
    plt.title("Distribution of Inventory Items by Hazard Class")
    plt.tight_layout()
    output_file = os.path.join(CONFIG['output_dir'], "hazard_distribution.png")
    plt.savefig(output_file)
    plt.close()

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
   
    
   
    import pandas as pd
    #Create a simple DataFrame for numerical data test
    numeric_test_data = pd.DataFrame({
        'ProductID': [101, 102, 103, 104],
        'Stock': [50, 20, 70, 35]
     })
    plot_stock_levels(numeric_test_data)
     
     # Create a simple DataFrame for categorical data test
    categorical_test_data = pd.DataFrame({
        'ProductID': [101, 102, 103, 104],
        'ProductName': ['Product A', 'Product B', 'Product C', 'Product D'],
        'Category': ['Electronics', 'Furniture', 'Clothing', 'Electronics'],
        'HazardClass': ['A', 'B', 'A', 'C'],
        'Supplier': ['Supplier X', 'Supplier Y', 'Supplier X', 'Supplier Z']
        })
    plot_hazard_distribution(categorical_test_data)
