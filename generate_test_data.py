# generate_test_data.py
import pandas as pd
import numpy as np

dates = pd.date_range(start="2025-01-01", periods=20, freq='D')
data = {
    "Date": dates.strftime('%Y-%m-%d'),
    "PM2.5": np.random.uniform(30, 60, size=20).round(1),
    "NO2": np.random.uniform(15, 30, size=20).round(1),
    "O3": np.random.uniform(25, 35, size=20).round(1),
    "Temperature": np.random.randint(10, 20, size=20)
}
df = pd.DataFrame(data)
df.to_csv("./Input/air_quality_data.csv", index=False)
print("Test data generated and saved!")
