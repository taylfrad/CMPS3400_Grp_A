#%% MODULE BEGINS
module_name_gl = 'inventory_numeric'

'''
Version: v0.3
Description:
    Parent/Child classes for numerical inventory processing,
    including all required plots and queries.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-07
Date Last Updated: 2025-05-05

Doc:
    InventoryNumeric: basic stats, histogram, line plot, simple search.
    InventoryNumericProcessor: adds violin, box, scatter, exports.
'''
#%% IMPORTS
import logging
import os
import pandas as pd
import matplotlib.pyplot as plt

from config import CONFIG
from visualization import save_plot

import ui
#%% CONSTANTS
# none
#%% CLASSES
class InventoryNumeric:
    def __init__(self, data: pd.DataFrame):
        logging.info("InventoryNumeric.__init__")
        self._data = data  # private-like attribute
        required = ['ProductID','Stock','Price','ReorderLevel']
        missing = [c for c in required if c not in data.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def calculate_total_stock(self) -> int:
        logging.info("calculate_total_stock called")
        return int(self._data['Stock'].sum())

    def calculate_average_price(self) -> float:
        logging.info("calculate_average_price called")
        return float(self._data['Price'].mean())

    def display_basic_stats(self):
        stats = {
            "Total Products": len(self._data),
            "Total Stock": self.calculate_total_stock(),
            "Average Price": f"${self.calculate_average_price():.2f}"
        }
        ui.display_report("BASIC INVENTORY STATISTICS", stats)

    def plot_histogram(self, col: str) -> str:
        logging.info(f"plot_histogram called on {col}")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.hist(self._data[col], bins=10)
        ax.set_title(f"{col} Histogram")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        return save_plot(fig, f"{col}_histogram.png")

    def plot_line(self, x_col: str, y_col: str) -> str:
        logging.info(f"plot_line called on {x_col} vs {y_col}")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(self._data[x_col], self._data[y_col], marker='o')
        ax.set_title(f"{y_col} vs {x_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        return save_plot(fig, f"{x_col}_{y_col}_line.png")

class InventoryNumericProcessor(InventoryNumeric):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        logging.info("InventoryNumericProcessor.__init__")

    def items_below_reorder(self) -> pd.DataFrame:
        logging.info("items_below_reorder called")
        return self._data.query("Stock < ReorderLevel")

    def generate_numeric_report(self) -> dict:
        logging.info("generate_numeric_report called")
        return {
            "Total Stock": self.calculate_total_stock(),
            "Average Price": round(self.calculate_average_price(),2),
            "Items Below Reorder": len(self.items_below_reorder())
        }

    def plot_violin(self, col: str) -> str:
        logging.info(f"plot_violin called on {col}")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.violinplot(self._data[col].dropna())
        ax.set_title(f"{col} Violin Plot")
        return save_plot(fig, f"{col}_violin.png")

    def plot_box(self, col: str) -> str:
        logging.info(f"plot_box called on {col}")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.boxplot(self._data[col].dropna())
        ax.set_title(f"{col} Box Plot")
        return save_plot(fig, f"{col}_box.png")

    def plot_scatter(self, x_col: str, y_col: str) -> str:
        logging.info(f"plot_scatter called on {x_col} vs {y_col}")
        fig, ax = plt.subplots(figsize=(6,4))
        ax.scatter(self._data[x_col], self._data[y_col])
        ax.set_title(f"{y_col} vs {x_col} Scatter")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        return save_plot(fig, f"{x_col}_{y_col}_scatter.png")

    def process_and_display(self):
        logging.info("process_and_display started")
        # Basic stats
        self.display_basic_stats()
        report = self.generate_numeric_report()
        ui.display_report("NUMERICAL INVENTORY REPORT", report)

        # Items below reorder
        below = self.items_below_reorder()
        if not below.empty:
            print("\nItems below reorder level:", flush=True)
            print(below[['ProductID','Stock','ReorderLevel']], flush=True)
        else:
            print("\nNo items below reorder level.", flush=True)

        # Advanced visualizations
        if ui.get_visualization_choice():
            try:
                logs = []
                logs.append(self.plot_histogram('Stock'))
                logs.append(self.plot_line('ProductID','Stock'))
                logs.append(self.plot_violin('Stock'))
                logs.append(self.plot_box('Stock'))
                logs.append(self.plot_scatter('ProductID','Price'))
                # export below-reorder as CSV
                out = os.path.join(CONFIG.output_dir, "below_reorder.csv")
                below.to_csv(out, index=False)
                logging.info(f"Exported below_reorder to {out}")
                ui.show_operation_status("Numeric advanced visualizations", True)
            except Exception as e:
                logging.error(f"Numeric viz error: {e}")
                ui.show_operation_status("Numeric advanced visualizations", False)

        logging.info("process_and_display completed")

#%% SELF-RUN
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = ui.load_data(CONFIG.inventory_numeric_csv, "numeric")
    if df is None:
        df = pd.DataFrame({
            'ProductID':[1,2,3],'Stock':[10,5,15],
            'Price':[9.99,19.99,4.99],'ReorderLevel':[8,7,10]
        })
    InventoryNumericProcessor(df).process_and_display()
