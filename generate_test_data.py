#Version: v0.1
#Date Last Updated: 2025-04-12

'''
Version: v0.1

Description:
    Generates comprehensive test data for the Inventory Management System.
    Two CSV files are generated:
      - inventory_numeric.csv: Contains numerical columns (ProductID, Stock, Price, ReorderLevel).
      - inventory_categorical.csv: Contains categorical columns (ProductID, ProductName, Category, HazardClass, Supplier).
      
    The HazardClass column is introduced for hazard classification (values A, B, C, D).
    
Authors:
   Taylor Fradella, Angel Njoku
Date Created     :  2025-04-07
Date Last Updated:  2025-04-12

Doc:
    Run this script to generate sample CSV data in the './Input' folder.
Notes:
    Make sure the Input folder exists or let the script create it.
'''

import pandas as pd
import numpy as np
import os
import random

# Ensure the Input folder exists
input_folder = "./Input"
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

# Define product categories and suppliers
categories = ["Electronics", "Chemicals", "Office Supplies", "Laboratory", "Furniture", "Cleaning", "Safety Equipment"]
suppliers = ["TechWorld Inc.", "ChemSupply Co.", "OfficeMax", "LabSource", "FurniTech", "CleanAll Ltd."]

# Define product names by category
product_names = {
    "Electronics": ["Desktop Computer", "Laptop", "Tablet", "Monitor", "Keyboard", "Mouse", "Printer", "Scanner", "UPS", "External Hard Drive"],
    "Chemicals": ["Hydrochloric Acid", "Sodium Hydroxide", "Ethanol", "Methanol", "Acetone", "Chloroform", "Formaldehyde", "Benzene", "Toluene", "Xylene"],
    "Office Supplies": ["Paper A4", "Paper A3", "Stapler", "Staples Box", "Pen Set", "Marker Set", "Scissors", "Tape Dispenser", "Binder Clips", "File Folders"],
    "Laboratory": ["Microscope", "Test Tubes", "Petri Dishes", "Pipettes", "Beakers", "Flask Set", "Bunsen Burner", "Centrifuge", "pH Meter", "Analytical Balance"],
    "Furniture": ["Office Desk", "Office Chair", "Bookshelf", "Filing Cabinet", "Conference Table", "Whiteboard", "Cork Board", "Standing Desk", "Sofa", "Coffee Table"],
    "Cleaning": ["All-Purpose Cleaner", "Glass Cleaner", "Floor Cleaner", "Disinfectant", "Hand Sanitizer", "Paper Towels", "Toilet Paper", "Trash Bags", "Dust Mop", "Wet Mop"],
    "Safety Equipment": ["First Aid Kit", "Fire Extinguisher", "Safety Goggles", "Face Shield", "Respirator", "Chemical Gloves", "Lab Coat", "Safety Helmet", "Ear Protection", "Emergency Eyewash"]
}

# Set hazard classes with appropriate associations
# A is highest hazard, D is lowest
hazard_class_by_category = {
    "Electronics": ["B", "C", "D"],        
    "Chemicals": ["A", "B"],                 
    "Office Supplies": ["C", "D"],           
    "Laboratory": ["A", "B", "C"],          
    "Furniture": ["C", "D"],                
    "Cleaning": ["B", "C"],                  
    "Safety Equipment": ["D"]                
}

# Generate data
num_products = 50
product_ids = list(range(101, 101 + num_products))

# Lists to store data
product_names_list = []
categories_list = []
hazard_classes_list = []
suppliers_list = []
stock_list = []
price_list = []
reorder_level_list = []

# Generate data for each product
for product_id in product_ids:
    # Select a random category
    category = random.choice(categories)
    categories_list.append(category)
    
    # Select a random product name from that category
    product_name = random.choice(product_names[category])
    product_names_list.append(product_name)
    
    # Assign an appropriate hazard class for this category
    hazard_class = random.choice(hazard_class_by_category[category])
    hazard_classes_list.append(hazard_class)
    
    # Select a random supplier
    supplier = random.choice(suppliers)
    suppliers_list.append(supplier)
    
    # Generate numeric data with realistic patterns
    # Higher hazard items tend to have lower stock and higher prices
    if hazard_class == 'A':
        stock = random.randint(5, 30)
        price = round(random.uniform(50, 300), 2)
        reorder_level = random.randint(10, 25)
    elif hazard_class == 'B':
        stock = random.randint(10, 50)
        price = round(random.uniform(30, 150), 2)
        reorder_level = random.randint(15, 35)
    elif hazard_class == 'C':
        stock = random.randint(20, 80)
        price = round(random.uniform(15, 100), 2)
        reorder_level = random.randint(20, 40)
    else:  # hazard_class == 'D'
        stock = random.randint(30, 100)
        price = round(random.uniform(5, 80), 2)
        reorder_level = random.randint(25, 50)
    
    # Ensure some items are below reorder level
    if random.random() < 0.15:  # 15% chance of being below reorder level
        stock = max(1, int(reorder_level * 0.8))
    
    stock_list.append(stock)
    price_list.append(price)
    reorder_level_list.append(reorder_level)

# Create the two DataFrames
numeric_data = pd.DataFrame({
    'ProductID': product_ids,
    'Stock': stock_list,
    'Price': price_list,
    'ReorderLevel': reorder_level_list
})

categorical_data = pd.DataFrame({
    'ProductID': product_ids,
    'ProductName': product_names_list,
    'Category': categories_list,
    'HazardClass': hazard_classes_list,
    'Supplier': suppliers_list
})

# Save to CSV files
numeric_data.to_csv(os.path.join(input_folder, "inventory_numeric.csv"), index=False)
categorical_data.to_csv(os.path.join(input_folder, "inventory_categorical.csv"), index=False)

print(f"Test data generated and saved to the '{input_folder}' folder.")
print(f"Generated {num_products} products across {len(categories)} categories.")
print(f"Hazard class distribution: {pd.Series(hazard_classes_list).value_counts().to_dict()}")
print(f"Items below reorder level: {sum(numeric_data['Stock'] < numeric_data['ReorderLevel'])}")