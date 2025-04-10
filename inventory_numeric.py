#Version: v0.1
#Date Last Updated: 2025-04-07

# Follow the coding standards listed in coding_standards.pdf 

#%% MODULE BEGINS
module_name_gl = 'inventory_numeric'

'''
Version: v0.1

Description:
    Module for processing numerical inventory data.
    This module defines a parent class for handling numerical data
    and a child class that extends it for analysis and reporting.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    Parent Class: InventoryNumeric - holds inventory numeric attributes and basic operations.
    Child Class: InventoryNumericProcessor - extends InventoryNumeric for detailed numeric reporting.
Notes:
    This module only handles columns such as ProductID, Stock, Price, and ReorderLevel.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pandas as pd

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (Not applicable)

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (None)

#%% CONFIGURATION               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (Configuration is in config.py)

#%% INITIALIZATIONS             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (None)

#%% DECLARATIONS                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# (No global declarations)

#%% CLASS DEFINITIONS           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class InventoryNumeric:
    def __init__(self, data):
        """
        INPUT:
            data (DataFrame): Must contain columns 'ProductID', 'Stock', 'Price', and 'ReorderLevel'
        """
        self.data = data

    def calculate_total_stock(self):
        """Returns the sum of the stock column."""
        return self.data['Stock'].sum()

    def calculate_average_price(self):
        """Returns the average price."""
        return self.data['Price'].mean()


class InventoryNumericProcessor(InventoryNumeric):
    def __init__(self, data):
        super().__init__(data)

    def items_below_reorder(self):
        """
        Returns a DataFrame with items where stock is below the reorder level.
        """
        return self.data[self.data['Stock'] < self.data['ReorderLevel']]

    def generate_numeric_report(self):
        """
        Generate a report containing:
          - Total Stock
          - Average Price
          - Count of items below reorder level
        """
        report = {
            "Total Stock": self.calculate_total_stock(),
            "Average Price": round(self.calculate_average_price(), 2),
            "Items Below Reorder": len(self.items_below_reorder())
        }
        return report

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # For testing purposes, create a synthetic DataFrame.
    test_data = pd.DataFrame({
        'ProductID': [101, 102, 103],
        'Stock': [50, 20, 70],
        'Price': [10.99, 15.49, 8.75],
        'ReorderLevel': [30, 25, 50]
    })
    processor = InventoryNumericProcessor(test_data)
    print("Numeric Report:", processor.generate_numeric_report())
