# Inventory Management System

**Course**: CMPS 3400  
**Team**: Group A  
**Contributors**: Taylor Fradella, Angel Njoku

## Project Overview

This project is a command-line based Inventory Management System developed in Python. It is capable of processing numerical and vector inventory data, performing statistical and vector analyses, and generating visual and tabular reports.

## Directory Structure

CMPS3400_Grp_A/
│
├── Input/ # Input CSV and pickle data files
├── Output/ # Generated reports and visualizations
├── Doc/ # Project documentation and final report
├── config.py # Configuration constants
├── inventory_numeric.py # Handles numeric data processing
├── inventory_vector.py # Handles vector data processing
├── main.py # Main program interface
└── ui.py # User input/output utilities

## Input Data Format

- CSV files for numeric inventory  
  Example columns: `ProductID`, `Stock`, `ReorderLevel`, `Price`
- Pickle files for vector data with attribute/label vectors

## Output Data Format

- `.csv` reports summarizing numeric analysis and probabilities
- `.jpg` images for histograms, line plots, scatter plots, etc.

## How to Run

Make sure Python 3 and required libraries are installed.

1. Clone the repository:

   git clone https://github.com/taylfrad/CMPS3400_Grp_A.git
   cd CMPS3400_Grp_A

2. Run the main interface:

   python main.py

   Follow the interactive menu to choose numeric or vector processing.

## Features

Numeric inventory statistics (total stock, reorder check, etc.)

Advanced statistical metrics (mean, median, std dev)

Vector math: dot product, projections, unit vectors, angle calc

Joint & conditional probabilities for categorical data

Data visualizations (histogram, line, scatter, violin, etc.)

Clean modular design with classes and inheritance

## Requirements

Python 3.x

pandas

matplotlib

numpy

Install required packages:

pip install pandas matplotlib numpy
