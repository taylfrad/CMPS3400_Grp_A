#Version: v0.1
#Date Last Updated: 2025-04-12

#%% MODULE BEGINS
module_name_gl = 'inventory_numeric'

'''
Version: v0.1

Description:
    Module for processing numerical inventory data.
    This module defines a parent class for handling numerical data
    and a child class that extends it for analysis and reporting.
    
Authors:
    Taylor Fradella, Angel Njoku
Date Created     :  2025-04-07
Date Last Updated:  2025-04-12

Doc:
    Parent Class: InventoryNumeric - holds inventory numeric attributes and basic operations.
    Child Class: InventoryNumericProcessor - extends InventoryNumeric for detailed numeric reporting.
Notes:
    This module only handles columns such as ProductID, Stock, Price, and ReorderLevel.
    Integrated with the ui.py module for user interaction.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd
import ui
from config import CONFIG


#%% CLASS DEFINITIONS           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class InventoryNumeric:
    def __init__(self, data):
        """
        Initialize the InventoryNumeric class with data.
        
        INPUT:
            data (DataFrame): Must contain columns 'ProductID', 'Stock', 'Price', and 'ReorderLevel'
        """
        self.data = data
        
        # Validate required columns
        required_columns = ['ProductID', 'Stock', 'Price', 'ReorderLevel']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            missing_cols_str = ', '.join(missing_columns)
            raise ValueError(f"Data is missing required columns: {missing_cols_str}")
    #

    def calculate_total_stock(self):
        """
        Calculate the sum of all stock quantities.
        
        INPUT: None
        OUTPUT:
            int: Total stock across all products
        """
        return self.data['Stock'].sum()
    #

    def calculate_average_price(self):
        """
        Calculate the average price of all products.
        
        INPUT: None
        OUTPUT:
            float: Average price
        """
        return self.data['Price'].mean()
    #
    
    def display_basic_stats(self):
        """
        Display basic statistics about the inventory using the UI module.
        
        INPUT: None
        OUTPUT: None
        """
        stats = {
            "Total Products": len(self.data),
            "Total Stock": self.calculate_total_stock(),
            "Average Price": f"${self.calculate_average_price():.2f}"
        }
        
        ui.display_report("BASIC INVENTORY STATISTICS", stats)
    #


class InventoryNumericProcessor(InventoryNumeric):
    def __init__(self, data):
        """
        Initialize the InventoryNumericProcessor with data.
        
        INPUT:
            data (DataFrame): Must contain columns 'ProductID', 'Stock', 'Price', and 'ReorderLevel'
        """
        super().__init__(data)
    #

    def items_below_reorder(self):
        """
        Find items where stock is below the reorder level.
        
        INPUT: None
        OUTPUT:
            DataFrame: Items with stock below reorder level
        """
        return self.data[self.data['Stock'] < self.data['ReorderLevel']]
    #

    def generate_numeric_report(self):
        """
        Generate a report containing total stock, average price, and items below reorder level.
        
        INPUT: None
        OUTPUT:
            dict: Report with numeric data analysis
        """
        report = {
            "Total Stock": self.calculate_total_stock(),
            "Average Price": round(self.calculate_average_price(), 2),
            "Items Below Reorder": len(self.items_below_reorder())
        }
        return report
    #
    
    def process_and_display(self):
        """
        Process numeric data and display results using the UI module.
        
        INPUT: None
        OUTPUT: None
        """
        # Generate report
        report = self.generate_numeric_report()
        
        # Display report using UI module
        ui.display_report("NUMERICAL INVENTORY REPORT", report)
        
        # Show items below reorder level
        items_below = self.items_below_reorder()
        if len(items_below) > 0:
            print("\nItems below reorder level:")
            print(items_below[['ProductID', 'Stock', 'ReorderLevel']])
        else:
            print("\nNo items are below reorder level.")
        
        # Ask if user wants to see visualization
        if ui.get_visualization_choice():
            try:
                from visualization import plot_stock_levels
                plot_stock_levels(self.data)
                ui.show_operation_status("Stock level visualization", True)
                ui.display_output_location()
            except Exception as e:
                print(f"Error generating visualization: {e}")
                ui.show_operation_status("Stock level visualization", False)
    #

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    
    # For testing purposes, create a synthetic DataFrame or load from file
    try:
        # Try to load from file first
        data = ui.load_data(CONFIG['inventory_numeric_csv'], "numeric")
        
        if data is None:
            # Use test data if file loading fails
            data = pd.DataFrame({
                'ProductID': [101, 102, 103],
                'Stock': [50, 20, 70],
                'Price': [10.99, 15.49, 8.75],
                'ReorderLevel': [30, 25, 50]
            })
            print("Using test data instead.")
        
        # Create processor and test functionality
        processor = InventoryNumericProcessor(data)
        processor.process_and_display()
        
    except Exception as e:
        print(f"Error during testing: {e}")