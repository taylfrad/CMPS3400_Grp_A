#%% MODULE BEGINS
module_name_gl = 'visualization'

'''
Version: v0.4
Description:
    Plotting utilities for inventory data.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-12
Date Last Updated: 2025-05-05

Doc:
    Bar, histogram, box, pie, violin, scatter, and line charts;
    all saved to CONFIG.output_dir.
'''
#%% IMPORTS
import logging
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from config import CONFIG
#%% CONSTANTS
HAZARD_COLORS = {'A': 'red', 'B': 'orange', 'C': 'gold', 'D': 'green'}
#%% HELPERS
def save_plot(fig, name: str) -> str:
    path = os.path.join(CONFIG.output_dir, name)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    logging.info(f"Plot saved: {path}")
    return path

#%% FUNCTIONS
def plot_histogram(df: pd.DataFrame, col: str) -> str:
    logging.info(f"plot_histogram called on {col}")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(df[col].dropna(), bins=10)
    ax.set_title(f"{col} Histogram")
    ax.set_xlabel(col); ax.set_ylabel("Frequency")
    return save_plot(fig, f"{col}_histogram.png")

def plot_line(df: pd.DataFrame, x_col: str, y_col: str) -> str:
    logging.info(f"plot_line called on {x_col} vs {y_col}")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(df[x_col], df[y_col], marker='o')
    ax.set_title(f"{y_col} vs {x_col}")
    ax.set_xlabel(x_col); ax.set_ylabel(y_col)
    return save_plot(fig, f"{x_col}_{y_col}_line.png")

def plot_stock_levels(df: pd.DataFrame) -> str:
    logging.info("plot_stock_levels called")
    fig, ax = plt.subplots(figsize=(12,6))
    data = df.sort_values('ProductID')
    ax.bar(data['ProductID'], data['Stock'])
    ax.set_xlabel("ProductID"); ax.set_ylabel("Stock")
    ax.set_title("Inventory Stock Levels")
    return save_plot(fig, "stock_levels.png")

def plot_violin(df: pd.DataFrame, col: str) -> str:
    logging.info(f"plot_violin called on {col}")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.violinplot(df[col].dropna())
    ax.set_title(f"{col} Violin Plot")
    return save_plot(fig, f"{col}_violin.png")

def plot_box(df: pd.DataFrame, col: str) -> str:
    logging.info(f"plot_box called on {col}")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.boxplot(df[col].dropna())
    ax.set_title(f"{col} Box Plot")
    return save_plot(fig, f"{col}_box.png")

def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str) -> str:
    logging.info(f"plot_scatter called on {x_col} vs {y_col}")
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(df[x_col], df[y_col])
    ax.set_title(f"{y_col} vs {x_col}")
    ax.set_xlabel(x_col); ax.set_ylabel(y_col)
    return save_plot(fig, f"{x_col}_{y_col}_scatter.png")

def plot_hazard_distribution(df: pd.DataFrame) -> str:
    logging.info("plot_hazard_distribution called")
    counts = df['HazardClass'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(counts.index, counts.values, color=[HAZARD_COLORS[c] for c in counts.index])
    ax.set_xlabel("HazardClass"); ax.set_ylabel("Count")
    ax.set_title("Distribution by Hazard Class")
    for i,v in enumerate(counts.values):
        ax.text(i, v+0.5, str(v), ha='center')
    return save_plot(fig, "hazard_distribution.png")

def plot_category_distribution(df: pd.DataFrame) -> str:
    logging.info("plot_category_distribution called")
    counts = df['Category'].value_counts()
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Distribution by Category")
    return save_plot(fig, "category_distribution.png")

def plot_price_by_hazard(merged: pd.DataFrame) -> str:
    logging.info("plot_price_by_hazard called")
    hazard = sorted(merged['HazardClass'].unique())
    data = [merged[merged['HazardClass']==h]['Price'] for h in hazard]
    fig, ax = plt.subplots(figsize=(6,4))
    ax.boxplot(data, labels=hazard, patch_artist=True)
    ax.set_xlabel("HazardClass"); ax.set_ylabel("Price")
    ax.set_title("Price Distribution by Hazard Class")
    avg = merged['Price'].mean()
    ax.axhline(avg, linestyle='--')
    ax.text(len(hazard)-1, avg*1.05, f"Avg: ${avg:.2f}")
    return save_plot(fig, "price_by_hazard.png")

def generate_combined_report(num_df: pd.DataFrame, cat_df: pd.DataFrame) -> dict:
    logging.info("generate_combined_report called")
    merged = pd.merge(num_df, cat_df, on='ProductID')
    p1 = plot_category_distribution(cat_df)
    p2 = plot_price_by_hazard(merged)
    summary = {
        "below_reorder": int((num_df['Stock']<num_df['ReorderLevel']).sum()),
        "high_hazard":  int((cat_df['HazardClass']=='A').sum()),
        "plots":       [p1, p2]
    }
    return summary

#%% SELF-RUN
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import ui
    # Load data for testing
    dn = ui.load_data(CONFIG.inventory_numeric_csv, "numeric")
    dc = ui.load_data(CONFIG.inventory_categorical_csv, "categorical")
    if dn is not None and dc is not None:
        generate_combined_report(dn, dc)
