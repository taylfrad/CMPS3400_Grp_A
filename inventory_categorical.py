# inventory_categorical.py
#Version: v0.1
#Date Last Updated: 2025-04-07

module_name_gl = 'inventory_categorical'

'''
Version: v0.1

Description:
    Module for processing categorical inventory data.
    Defines a parent class for handling descriptive data (ProductName, Category, etc.)
    and a child class extending this to include hazard class categorization.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    Parent Class: InventoryCategorical
    Child Class: InventoryCategoricalProcessor
    The child class now provides a method to group items by HazardClass.
Notes:
    Uses a new column 'HazardClass' that can hold values A, B, C, or D.
'''

import pandas as pd

class InventoryCategorical:
    def __init__(self, data):
        """
        INPUT:
            data (DataFrame): Must contain columns:
                - ProductID
                - ProductName
                - Category
                - HazardClass (A, B, C, or D)
                - Supplier
        """
        self.data = data

    def count_by_category(self):
        """Returns a Series counting items by 'Category'."""
        return self.data.groupby("Category").size()

    def count_by_supplier(self):
        """Returns a Series counting items by 'Supplier'."""
        return self.data.groupby("Supplier").size()

class InventoryCategoricalProcessor(InventoryCategorical):
    def __init__(self, data):
        super().__init__(data)

    def count_by_hazard_class(self):
        """Returns a Series counting how many items fall under each HazardClass."""
        return self.data.groupby("HazardClass").size()

    def generate_category_report(self):
        """
        Generate a report containing:
          - Counts of items by category
          - Counts of items by supplier
          - Counts of items by hazard class
        """
        report = {
            "Items by Category": self.count_by_category().to_dict(),
            "Items by Supplier": self.count_by_supplier().to_dict(),
            "Items by HazardClass": self.count_by_hazard_class().to_dict()
        }
        return report

if __name__ == "__main__":
    test_data = pd.DataFrame({
        'ProductID': [101, 102, 103, 104],
        'ProductName': ['Paper Towels', 'Cooking Oil', 'Laptop', 'Magnesium Strips'],
        'Category': ['Cleaning Supplies', 'Kitchen Supplies', 'Office Supplies', 'Lab Supplies'],
        'HazardClass': ['A', 'B', 'C', 'D'],
        'Supplier': ['Supplier X', 'Supplier Y', 'Supplier Z', 'Supplier A']
    })

    processor = InventoryCategoricalProcessor(test_data)
    report = processor.generate_category_report()
    print("Categorical Report:", report)
