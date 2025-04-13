#Version: v0.2
#Date Last Updated: 2025-04-12

module_name_gl = 'visualization'

'''
Version: v0.2

Description:
    Module for visualizing inventory management data.
    
Authors:
    Taylor Fradella, Angel Njoku
Date Last Updated: 2025-04-12
'''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from config import CONFIG

# Create output directory if it doesn't exist
os.makedirs(CONFIG['output_dir'], exist_ok=True)

# Hazard class colors for consistent visualization
HAZARD_COLORS = {
    'A': 'red',
    'B': 'orange',
    'C': 'gold',
    'D': 'green'
}

def save_plot(filename):
    """Helper function to save plots to the output directory."""
    output_path = os.path.join(CONFIG['output_dir'], filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path

def plot_stock_levels(numeric_data):
    """
    Plot a simple inventory stock level by product item.
    
    INPUT:
        numeric_data (DataFrame): Must contain columns 'ProductID' and 'Stock'
    
    OUTPUT:
        str: Path to the saved plot file
    """
    # Sort by ProductID for better presentation
    sorted_data = numeric_data.sort_values('ProductID')
    
    # Create figure with better dimensions for readability
    plt.figure(figsize=(14, 8))
    
    # Use a cleaner style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Create the x positions
    x = np.arange(len(sorted_data))
    width = 0.7
    
    # Create bars with a single color
    bars = plt.bar(
        x, 
        sorted_data['Stock'],
        width=width,
        color='#3498db',  # Blue color for all bars
        alpha=0.8
    )
    
    # Add stock values as text labels
    for i, (idx, row) in enumerate(sorted_data.iterrows()):
        # Add stock labels directly on the bars
        plt.text(
            x[i], 
            row['Stock'] + 2,  # Place text above the bar
            f"{int(row['Stock'])}",
            ha='center',
            va='bottom',
            color='black',
            fontweight='bold',
            fontsize=9
        )
    
    # Better labels and title with improved formatting
    plt.xlabel("Product ID", fontsize=12, fontweight='bold')
    plt.ylabel("Quantity in Stock", fontsize=12, fontweight='bold')
    plt.title("Inventory Stock Levels by Product", fontsize=16, fontweight='bold', pad=20)
    
    # Set x-ticks to product IDs with better spacing
    # If many products, show a subset of IDs to avoid overcrowding
    if len(sorted_data) > 30:
        # Show every 5th product ID for readability
        plt.xticks(x[::5], sorted_data['ProductID'].iloc[::5])
    else:
        plt.xticks(x, sorted_data['ProductID'])
    
    # Add grid for easier comparison
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add some padding to the y-axis
    plt.ylim(0, max(sorted_data['Stock']) * 1.15)
    
    plt.tight_layout()
    
    # Save the figure
    output_file = os.path.join(CONFIG['output_dir'], "stock_levels.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    return output_file

def plot_hazard_distribution(categorical_data):
    """Plot distribution of items by hazard class."""
    # Count items in each hazard class
    hazard_counts = categorical_data['HazardClass'].value_counts().sort_index()
    
    plt.figure(figsize=(8, 6))
    bars = hazard_counts.plot(kind='bar', color=[HAZARD_COLORS.get(cls, 'blue') 
                                               for cls in hazard_counts.index])
    
    # Add count labels on bars
    for i, count in enumerate(hazard_counts):
        plt.text(i, count + 0.5, str(count), ha='center', fontweight='bold')
    
    plt.xlabel("Hazard Class (A=Highest, D=Lowest)")
    plt.ylabel("Number of Items")
    plt.title("Distribution of Items by Hazard Class")
    
    return save_plot("hazard_distribution.png")

def plot_category_distribution(categorical_data):
    """Create a pie chart of items by category."""
    category_counts = categorical_data['Category'].value_counts()
    
    plt.figure(figsize=(9, 7))
    plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%',
            startangle=90, shadow=True)
    plt.axis('equal')
    plt.title("Distribution of Items by Category")
    
    return save_plot("category_distribution.png")

def plot_price_by_hazard(merged_data):
    """Create a box plot of prices by hazard class."""
    plt.figure(figsize=(8, 6))
    
    # Sort hazard classes
    hazard_order = sorted(merged_data['HazardClass'].unique())
    
    # Create boxplot with colored boxes
    boxplot = plt.boxplot([merged_data[merged_data['HazardClass'] == cls]['Price'] 
                         for cls in hazard_order], labels=hazard_order, patch_artist=True)
    
    # Color boxes by hazard class
    for i, box in enumerate(boxplot['boxes']):
        box.set(facecolor=HAZARD_COLORS.get(hazard_order[i], 'blue'))
    
    plt.xlabel("Hazard Class")
    plt.ylabel("Price ($)")
    plt.title("Price Distribution by Hazard Class")
    
    # Add average price line
    avg_price = merged_data['Price'].mean()
    plt.axhline(y=avg_price, color='blue', linestyle='--', alpha=0.7)
    plt.text(len(hazard_order)-0.5, avg_price*1.1, f'Avg: ${avg_price:.2f}', color='blue')
    
    return save_plot("price_by_hazard.png")

def generate_combined_report(numeric_data, categorical_data):
    """Generate and display combined analysis of both datasets."""
    # Merge datasets
    merged_data = pd.merge(numeric_data, categorical_data, on='ProductID')
    
    # Generate visualizations
    category_plot = plot_category_distribution(categorical_data)
    price_plot = plot_price_by_hazard(merged_data)
    
    # Calculate key metrics
    below_reorder = len(numeric_data[numeric_data['Stock'] < numeric_data['ReorderLevel']])
    high_hazard = len(categorical_data[categorical_data['HazardClass'] == 'A'])
    
    # Print summary
    print("\nInventory Summary:")
    print(f"Total Products: {len(merged_data)}")
    print(f"Total Stock: {numeric_data['Stock'].sum()}")
    print(f"Average Price: ${numeric_data['Price'].mean():.2f}")
    print(f"Items Below Reorder Level: {below_reorder}")
    print(f"High Hazard Items (Class A): {high_hazard}")
    
    # Return summary data
    return {
        "visualizations": ["category_distribution.png", "price_by_hazard.png"],
        "below_reorder": below_reorder,
        "high_hazard": high_hazard
    }

if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
   
    # Create test data
    numeric_test = pd.DataFrame({
        'ProductID': [101, 102, 103, 104],
        'Stock': [50, 20, 70, 35],
        'Price': [24.99, 124.50, 9.99, 45.00],
        'ReorderLevel': [40, 30, 50, 30]
    })
    
    categorical_test = pd.DataFrame({
        'ProductID': [101, 102, 103, 104],
        'ProductName': ['Product A', 'Product B', 'Product C', 'Product D'],
        'Category': ['Electronics', 'Furniture', 'Cleaning', 'Electronics'],
        'HazardClass': ['A', 'B', 'A', 'C'],
        'Supplier': ['TechWorld Inc.', 'FurniTech', 'CleanAll Ltd.', 'TechWorld Inc.']
    })
    
    # Test visualizations
    print("Testing all visualizations...")
    plot_stock_levels(numeric_test)
    plot_hazard_distribution(categorical_test)
    generate_combined_report(numeric_test, categorical_test)
    print("All visualizations created successfully.")