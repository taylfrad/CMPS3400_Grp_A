#Version: v0.1
#Date Last Updated: 2025-04-07

'''
Version: v0.1

Description:
    Generates synthetic test data for the Inventory Management System.
    Two CSV files are generated:
      - inventory_numeric.csv: Contains numerical columns (ProductID, Stock, Price, ReorderLevel).
      - inventory_categorical.csv: Contains categorical columns (ProductID, ProductName, Category, HazardClass, Supplier).
      
    The HazardClass column is introduced for hazard classification (values A, B, C, D) as per professor's requirements.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    Run this script to generate sample CSV data in the './Input' folder.
Notes:
    Make sure the Input folder exists or let the script create it.
'''

import pandas as pd
import numpy as np
import os

# Ensure the Input folder exists
input_folder = "./Input"
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

# Generate numerical inventory data
numeric_data = pd.DataFrame({
    'ProductID': np.arange(101, 111),  # Produces Product IDs from 101 to 110
    'Stock': np.random.randint(10, 100, 10),
    'Price': np.round(np.random.uniform(5, 25, 10), 2),
    'ReorderLevel': np.random.randint(20, 50, 10)
})
numeric_data.to_csv(os.path.join(input_folder, "inventory_numeric.csv"), index=False)

# Define hazard classes and generate categorical inventory data
hazard_classes = ['A', 'B', 'C', 'D']
categorical_data = pd.DataFrame({
    'ProductID': np.arange(101, 111),
    'ProductName': [f"Product {i}" for i in range(1, 11)],
    'Category': np.random.choice(['Electronics', 'Furniture', 'Clothing'], 10),
    'HazardClass': np.random.choice(hazard_classes, 10),
    'Supplier': np.random.choice(['Supplier A', 'Supplier B', 'Supplier C'], 10)
})
categorical_data.to_csv(os.path.join(input_folder, "inventory_categorical.csv"), index=False)

print("Test data generated and saved to the './Input' folder.")
