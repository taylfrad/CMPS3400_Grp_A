#%% MODULE BEGINS
module_name_gl = 'ui'

'''
Version: v0.3
Description:
    CLI interface for Inventory Management.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-12
Date Last Updated: 2025-05-XX

Doc:
    Menus, prompts, report formatting, and file checks.
'''
#%% IMPORTS
import os
import pandas as pd

from config import CONFIG
#%% CONSTANTS
COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m"
}
#%% FUNCTIONS
def display_welcome_message():
    print("\n" + "="*60, flush=True)
    print("INVENTORY MANAGEMENT SYSTEM".center(60), flush=True)
    print("="*60 + "\n", flush=True)

def display_menu():
    print("\nMAIN MENU:", flush=True)
    print("1. Process Numerical Data", flush=True)
    print("2. Process Vector (pickle) Data", flush=True)
    print("3. Run All", flush=True)
    print("4. Exit", flush=True)

def get_user_choice():
    while True:
        try:
            c = int(input("Choice (1-4): "))
            if 1 <= c <= 4:
                return c
        except:
            pass
        print("Enter a number 1–4.", flush=True)

def confirm_file_paths():
    csv_exists = os.path.exists(CONFIG.inventory_numeric_csv)
    pkl_exists = os.path.exists(CONFIG.input_pickle)
    missing = []
    if not csv_exists:
        missing.append(CONFIG.inventory_numeric_csv)
    if not pkl_exists:
        missing.append(CONFIG.input_pickle)
    if missing:
        print("\nWARNING: Missing input files:", flush=True)
        for m in missing:
            print(f"  - {m}", flush=True)
        return input("Continue anyway? (y/n): ").lower() == 'y'
    return True

def load_data(path: str, dtype: str):
    try:
        df = pd.read_csv(path)
        print(f"Loaded {dtype} data from {path} ({len(df)} rows)", flush=True)
        return df
    except Exception as e:
        print(f"Error loading {dtype} data: {e}", flush=True)
        return None

def get_visualization_choice(auto=False):
    if auto:
        return True
    return input("Generate visualizations? (y/n): ").lower() == 'y'

def display_report(title: str, data: dict):
    print("\n" + "-"*60, flush=True)
    print(title.center(60), flush=True)
    print("-"*60, flush=True)
    for k, v in data.items():
        if isinstance(v, dict):
            print(f"{k}:", flush=True)
            for sk, sv in v.items():
                print(f"  {sk}: {sv}", flush=True)
        else:
            print(f"{k}: {v}", flush=True)
    print("-"*60, flush=True)

def show_operation_status(operation: str, success: bool):
    status = f"{COLORS['GREEN']}SUCCESS{COLORS['RESET']}" if success else f"{COLORS['RED']}FAILED{COLORS['RESET']}"
    print(f"{operation}: {status}", flush=True)

def display_output_location():
    print(f"\nOutputs saved in: {os.path.abspath(CONFIG.output_dir)}", flush=True)

def display_run_all_banner():
    print("\n" + "="*60, flush=True)
    print(f"{COLORS['BOLD']}RUN ALL ANALYSIS{COLORS['RESET']}".center(60), flush=True)
    print("="*60, flush=True)

def display_processing_complete():
    print("\n" + "="*60, flush=True)
    print(f"{COLORS['GREEN']}PROCESSING COMPLETE{COLORS['RESET']}".center(60), flush=True)
    print("="*60, flush=True)
    display_output_location()
    print("="*60, flush=True)

#%% SELF-RUN
if __name__ == "__main__":
    display_welcome_message()
    display_menu()
    display_run_all_banner()
    display_processing_complete()
