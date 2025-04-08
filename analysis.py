# analysis.py
def compute_statistics(data):
    """
    Computes summary statistics for air quality data.
    
    INPUT:
        data (DataFrame): The DataFrame with air quality metrics.
    OUTPUT:
        dict: Dictionary containing computed statistics.
    """
    stats = {
        'mean_pm25': data['PM2.5'].mean(),
        'median_pm25': data['PM2.5'].median(),
        'std_pm25': data['PM2.5'].std()
    }
    return stats
