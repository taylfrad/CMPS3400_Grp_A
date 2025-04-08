#Version: v0.1
#Date Last Updated: 2025-04-07

#%% MODULE BEGINS
module_name_gl = 'visualization'

'''
Version: v0.1

Description:
    Module for visualizing air quality data.
    
Authors:
    Taylor Fradella
Date Created     :  2025-04-07
Date Last Updated:  2025-04-07

Doc:
    Provides functions to plot air quality measurements and save the generated plots.
Notes:
    Ensure that the plots are properly labeled and saved in the output directory.
'''

#%% IMPORTS                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import os
from config import CONFIG

#%% FUNCTION DEFINITIONS        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def plot_air_quality(data, stats):
    """
    Plots air quality data and saves the visualization.
    
    INPUT:
        data (DataFrame): Air quality data with 'Date' and 'PM2.5' columns.
        stats (dict): Dictionary of computed statistics.
    
    OUTPUT:
        None: Saves the generated plot to the output directory.
    """
    # Example: Plot PM2.5 levels over time
    plt.figure()
    plt.plot(data['Date'], data['PM2.5'], label='PM2.5 Levels')
    plt.xlabel("Date")
    plt.ylabel("PM2.5")
    plt.title("Urban Air Quality Over Time")
    plt.legend()
    
    # Construct output file path and save the figure
    output_file = os.path.join(CONFIG['output_dir'], "pm25_over_time.png")
    plt.savefig(output_file)
    plt.close()

#%% SELF-RUN                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    print(f"\"{module_name_gl}\" module begins.")
    # For testing, load sample data and call plot_air_quality if desired.
