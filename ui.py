#Version: v0.1
#Date Last Updated: 2025-04-12

#%% MODULE BEGINS
module_name_gl = 'ui'

'''
Version: v0.1

Description:
    User interface module for the Inventory Management System.
    Provides functionality for user interaction, input collection,
    and displaying results to the user.
    
Authors:
    Taylor Fradella, Angel Njoku
Date Created     :  2025-04-12
Date Last Updated:  2025-04-12

Doc:
    This module contains functions for displaying menus, collecting user input,
    and formatting outputs for the Inventory Management System.
Notes:
    Used by both the numeric and categorical processing modules to handle user interaction.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import pandas as pd
from config import CONFIG

#%% USER INTERFACE              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def display_welcome_message():
    """
    Display a welcome message to the user.
    
    INPUT: None
    OUTPUT: None
    """
    print("\n" + "="*60)
    print("INVENTORY MANAGEMENT SYSTEM".center(60))
    print("="*60)
    print("This program analyzes inventory data and generates reports.")
    print("="*60 + "\n")
#

def display_menu():
    """
    Display the main menu options to the user.
    
    INPUT: None
    OUTPUT: None
    """
    print("\nMAIN MENU:")
    print("1. Process Numerical Inventory Data")
    print("2. Process Categorical Inventory Data")
    print("3. Process Both Types of Data")
    print("4. Run All (Process Data & Generate All Reports)")
    print("5. Exit Program")
#

def get_user_choice():
    """
    Get the user's menu choice.
    
    INPUT: None
    OUTPUT: 
        choice (int): User's menu choice (1-5)
    """
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Error: Please enter a number between 1 and 5.")
        except ValueError:
            print("Error: Please enter a valid number.")
#

def display_report(report_title, report_data):
    """
    Display a formatted report to the user.
    
    INPUT: 
        report_title (str): Title of the report
        report_data (dict): Dictionary containing report data
    OUTPUT: None
    """
    print("\n" + "-"*60)
    print(f"{report_title}".center(60))
    print("-"*60)
    
    for key, value in report_data.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {subvalue}")
        else:
            print(f"{key}: {value}")
    
    print("-"*60)
#

def confirm_file_paths():
    """
    Confirm that data files exist and prompt user to continue.
    
    INPUT: None
    OUTPUT:
        bool: True if files exist or user chooses to continue, False otherwise
    """
    numeric_file = CONFIG["inventory_numeric_csv"]
    categorical_file = CONFIG["inventory_categorical_csv"]
    
    files_exist = os.path.exists(numeric_file) and os.path.exists(categorical_file)
    
    if not files_exist:
        print("\nWARNING: One or more data files not found:")
        if not os.path.exists(numeric_file):
            print(f"  - {numeric_file} not found")
        if not os.path.exists(categorical_file):
            print(f"  - {categorical_file} not found")
        
        response = input("\nWould you like to continue anyway? (y/n): ").lower()
        return response == 'y'
    
    return True
#

def load_data(file_path, data_type):
    """
    Load data from a CSV file and display a message.
    
    INPUT: 
        file_path (str): Path to the CSV file
        data_type (str): Type of data being loaded ("numeric" or "categorical")
    OUTPUT:
        DataFrame or None: Loaded data if successful, None otherwise
    """
    try:
        data = pd.read_csv(file_path)
        print(f"\nSuccessfully loaded {data_type} data from {file_path}")
        print(f"Found {len(data)} records.")
        return data
    except Exception as e:
        print(f"\nError loading {data_type} data: {e}")
        return None
#

#%% CONSTANTS                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Terminal colors for output formatting
COLORS_UI = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m"
}

#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_visualization_choice(auto_yes=False):
    """
    Ask user if they want to generate visualizations.
    
    INPUT: 
        auto_yes (bool): If True, automatically return True without asking
    OUTPUT:
        bool: True if user wants visualizations, False otherwise
    """
    if auto_yes:
        return True
        
    while True:
        response = input("\nGenerate visualizations? (y/n): ").lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' for yes or 'n' for no.")
#

def show_operation_status(operation, success):
    """
    Display operation status with appropriate formatting.
    
    INPUT:
        operation (str): Description of the operation
        success (bool): Whether the operation was successful
    OUTPUT: None
    """
    status = f"{COLORS_UI['GREEN']}SUCCESS{COLORS_UI['RESET']}" if success else f"{COLORS_UI['RED']}FAILED{COLORS_UI['RESET']}"
    print(f"{operation}: {status}")
#

def display_output_location():
    """
    Inform the user where output files are saved.
    
    INPUT: None
    OUTPUT: None
    """
    print(f"\nOutput files are saved to: {os.path.abspath(CONFIG['output_dir'])}")
#

def display_run_all_banner():
    """
    Display a banner for the Run All option.
    
    INPUT: None
    OUTPUT: None
    """
    print("\n" + "="*60)
    print(f"{COLORS_UI['BOLD']}RUNNING COMPLETE INVENTORY ANALYSIS{COLORS_UI['RESET']}".center(60))
    print("="*60)
    print("Processing all data, generating reports and visualizations...")
    print("="*60)
#

def display_processing_complete():
    """
    Display a message indicating that processing is complete.
    
    INPUT: None
    OUTPUT: None
    """
    print("\n" + "="*60)
    print(f"{COLORS_UI['GREEN']}PROCESSING COMPLETE{COLORS_UI['RESET']}".center(60))
    print("="*60)
    print(f"All reports and visualizations have been generated.")
    display_output_location()
    print("="*60)
#

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    
    # Test UI functions
    display_welcome_message()
    display_menu()
    
    print("\nTesting report display:")
    test_report = {
        "Total Items": 10,
        "Categories": {
            "Electronics": 5,
            "Furniture": 3,
            "Clothing": 2
        },
        "Average Price": 24.99
    }
    display_report("TEST REPORT", test_report)
    
    print("\nCheck color output:")
    for color_name, color_code in COLORS_UI.items():
        if color_name != "RESET":
            print(f"{color_code}This text should be in {color_name}{COLORS_UI['RESET']}")
            
    # Test Run All banner
    display_run_all_banner()
    display_processing_complete()