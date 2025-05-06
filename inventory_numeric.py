# inventory_numeric.py
#%% MODULE BEGINS
module_name_gl = 'inventory_numeric'

'''
Version: v0.6
Description:
    Parent/Child classes for numerical inventory processing,
    including full stats, query features, probability calculations,
    and required plots & exports.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-07
Date Last Updated: 2025-05-06

Doc:
    InventoryNumeric: basic & extended stats, histogram, line plot.
    InventoryNumericProcessor: reorder checks, joint/conditional probabilities,
      median, std-dev, CSV export, and advanced visualizations.
'''
#%% IMPORTS
import logging
import os
import pandas as pd
import matplotlib.pyplot as plt

from config import CONFIG
from visualization import save_plot
import ui

#%% CLASSES
class InventoryNumeric:
    def __init__(self, data: pd.DataFrame):
        logging.info("InventoryNumeric.__init__")
        self._data = data
        required = ['ProductID', 'Stock', 'Price', 'ReorderLevel']
        missing = [c for c in required if c not in data.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def calculate_total_stock(self) -> int:
        logging.info("calculate_total_stock called")
        return int(self._data['Stock'].sum())

    def calculate_average_price(self) -> float:
        logging.info("calculate_average_price called")
        return float(self._data['Price'].mean())

    def calculate_median_price(self) -> float:
        logging.info("calculate_median_price called")
        return float(self._data['Price'].median())

    def calculate_std_price(self) -> float:
        logging.info("calculate_std_price called")
        return float(self._data['Price'].std())

    def display_basic_stats(self):
        stats = {
            "Total Products": len(self._data),
            "Total Stock": self.calculate_total_stock(),
            "Average Price": f"${self.calculate_average_price():.2f}",
            "Median Price": f"${self.calculate_median_price():.2f}",
            "Std Dev Price": f"${self.calculate_std_price():.2f}"
        }
        ui.display_report("BASIC INVENTORY STATISTICS", stats)

    def plot_histogram(self, col: str) -> str:
        logging.info(f"plot_histogram called on {col}")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(self._data[col], bins=10)
        ax.set_title(f"{col} Histogram")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        return save_plot(fig, f"{col}_histogram.png")

    def plot_line(self, x_col: str, y_col: str) -> str:
        logging.info(f"plot_line called on {x_col} vs {y_col}")
        fig, ax = plt.subplots(figsize=(6, 4))
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
            "Average Price": round(self.calculate_average_price(), 2),
            "Items Below Reorder": len(self.items_below_reorder())
        }

    def process_and_display(self):
        logging.info("process_and_display started")

        # Basic & extended stats
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

        # Determine dynamic numeric columns for joint/conditional probabilities
        num_cols = self._data.select_dtypes(include='number').columns.tolist()
        num_cols = [c for c in num_cols if c not in ['ProductID','ReorderLevel']]
        if len(num_cols) >= 2:
            col1, col2 = num_cols[0], num_cols[1]
            total = len(self._data)
            jc = self._data.groupby([col1, col2]).size()

            print("\n------------------------------------------------------------", flush=True)
            print("                        Joint Counts", flush=True)
            print("------------------------------------------------------------", flush=True)
            for (a, b), cnt in jc.items():
                print(f"({a}, {b}): {cnt}", flush=True)

            print("\n------------------------------------------------------------", flush=True)
            print("                     Joint Probabilities", flush=True)
            print("------------------------------------------------------------", flush=True)
            for (a, b), cnt in jc.items():
                print(f"({a}, {b}): {cnt/total:.2f}", flush=True)

            # Conditional probabilities P(col1|col2)
            marg = self._data.groupby(col2).size()
            print("\n------------------------------------------------------------", flush=True)
            print("                 Conditional Probabilities", flush=True)
            print("------------------------------------------------------------", flush=True)
            for (a, b), cnt in jc.items():
                cond = cnt / marg[b]
                print(f"P({a}|{b}) = {cond:.2f}", flush=True)
        else:
            print("\nNot enough numeric columns for joint counts & probabilities.", flush=True)

        # Advanced visualizations
        if ui.get_visualization_choice():
            try:
                self.plot_histogram('Stock')
                self.plot_line('ProductID', 'Stock')
                self.plot_histogram('Price')
                self.plot_line('ProductID', 'Price')
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
            'ProductID': [1, 2, 3],
            'Stock': [10, 5, 15],
            'Price': [9.99, 19.99, 4.99],
            'ReorderLevel': [8, 7, 10]
        })
    InventoryNumericProcessor(df).process_and_display()