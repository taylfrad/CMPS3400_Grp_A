import pandas as pd

df = pd.DataFrame({
    'VectorA': [1, 2, 3],
    'VectorB': [4, 5, 6],
    'Category': ['X', 'Y', 'Z']
})

df.to_pickle('./Input/vector_test_data.pkl')
print("Pickle file saved to ./Input/vector_test_data.pkl")
