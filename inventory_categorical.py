#Version: v0.1
#Date Last Updated: 2025-04-12

#%% MODULE BEGINS
module_name_gl = 'inventory_categorical'

'''
Version: v0.1

Description:
    Module for processing categorical inventory data.
    Defines a parent class for handling descriptive data (ProductName, Category, etc.)
    and a child class extending this to include hazard class categorization.
    
Authors:
    Taylor Fradella, Angel Njoku
Date Created     :  2025-04-07
Date Last Updated:  2025-04-12

Doc:
    Parent Class: InventoryCategorical - handles basic categorical data operations
    Child Class: InventoryCategoricalProcessor - extends functionality for hazard classification
    The child class provides a method to group items by HazardClass.
Notes:
    Uses a 'HazardClass' column that can hold values A, B, C, or D.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd
import ui
from config import CONFIG


#%% CLASS DEFINITIONS           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class InventoryCategorical:
    def __init__(self, data):
        """
        Initialize the InventoryCategorical class with data.
        
        INPUT:
            data (DataFrame): Must contain columns:
                - ProductID
                - ProductName
                - Category
                - HazardClass (A, B, C, or D)
                - Supplier
        """
        self.data = data
        
        # Validate required columns
        required_columns = ['ProductID', 'ProductName', 'Category', 'HazardClass', 'Supplier']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            missing_cols_str = ', '.join(missing_columns)
            raise ValueError(f"Data is missing required columns: {missing_cols_str}")
    #

    def count_by_category(self):
        """
        Count items by Category.
        
        INPUT: None
        OUTPUT:
            Series: Counts of items by Category
        """
        return self.data.groupby("Category").size()
    #

    def count_by_supplier(self):
        """
        Count items by Supplier.
        
        INPUT: None
        OUTPUT:
            Series: Counts of items by Supplier
        """
        return self.data.groupby("Supplier").size()
    #
    
    def display_basic_stats(self):
        """
        Display basic statistics about categorical data using the UI module.
        
        INPUT: None
        OUTPUT: None
        """
        stats = {
            "Total Products": len(self.data),
            "Number of Categories": len(self.data['Category'].unique()),
            "Number of Suppliers": len(self.data['Supplier'].unique())
        }
        
        ui.display_report("BASIC CATEGORICAL STATISTICS", stats)
    #

class InventoryCategoricalProcessor(InventoryCategorical):
    def __init__(self, data):
        """
        Initialize the InventoryCategoricalProcessor with data.
        
        INPUT:
            data (DataFrame): Must contain required columns from parent class
        """
        super().__init__(data)
    #

    def count_by_hazard_class(self):
        """
        Count items by HazardClass.
        
        INPUT: None
        OUTPUT:
            Series: Counts of items by HazardClass
        """
        return self.data.groupby("HazardClass").size()
    #

    def generate_category_report(self):
        """
        Generate a report with counts by category, supplier, and hazard class.
        
        INPUT: None
        OUTPUT:
            dict: Report with categorical data analysis
        """
        report = {
            "Items by Category": self.count_by_category().to_dict(),
            "Items by Supplier": self.count_by_supplier().to_dict(),
            "Items by HazardClass": self.count_by_hazard_class().to_dict()
        }
        return report
    #
    
    def process_and_display(self):
        """
        Process categorical data and display results using the UI module.
        
        INPUT: None
        OUTPUT: None
        """
        # Generate report
        report = self.generate_category_report()
        
        # Display report using UI module
        ui.display_report("CATEGORICAL INVENTORY REPORT", report)
        
        # Show detailed information about high hazard items (class A)
        high_hazard_items = self.data[self.data['HazardClass'] == 'A']
        if len(high_hazard_items) > 0:
            print("\nHigh hazard items (Class A):")
            print(high_hazard_items[['ProductID', 'ProductName', 'Category', 'Supplier']])
        else:
            print("\nNo Class A (high hazard) items found.")
        
        # Ask if user wants to see visualization
        if ui.get_visualization_choice():
            try:
                from visualization import plot_hazard_distribution
                plot_hazard_distribution(self.data)
                ui.show_operation_status("Hazard distribution visualization", True)
                ui.display_output_location()
            except Exception as e:
                print(f"Error generating visualization: {e}")
                ui.show_operation_status("Hazard distribution visualization", False)
    #

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    
    # For testing purposes, create a synthetic DataFrame or load from file
    try:
        # Try to load from file first
        data = ui.load_data(CONFIG['inventory_categorical_csv'], "categorical")
        
        if data is None:
            # Use test data if file loading fails
            data = pd.DataFrame({
                'ProductID': [101, 102, 103, 104],
                'ProductName': ['Paper Towels', 'Cooking Oil', 'Laptop', 'Magnesium Strips'],
                'Category': ['Cleaning Supplies', 'Kitchen Supplies', 'Office Supplies', 'Lab Supplies'],
                'HazardClass': ['A', 'B', 'C', 'D'],
                'Supplier': ['Supplier X', 'Supplier Y', 'Supplier Z', 'Supplier A']
            })
            print("Using test data instead.")
        
        # Create processor and test functionality
        processor = InventoryCategoricalProcessor(data)
        processor.process_and_display()
        
    except Exception as e:
        print(f"Error during testing: {e}")