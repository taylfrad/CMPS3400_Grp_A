# inventory_vector.py
import pandas as pd
import numpy as np
import math
from itertools import combinations, permutations

class InventoryVector:
    def __init__(self, data):
        self.data = data

    def mean(self, col):
        return self.data[col].mean()

    def std(self, col):
        return self.data[col].std()

    def joint_counts(self, col1, col2):
        return self.data.groupby([col1, col2]).size()

    def joint_probabilities(self, col1, col2):
        return self.joint_counts(col1, col2) / len(self.data)

    def conditional_probability(self, target_col, given_col):
        cond_prob = self.data.groupby(given_col)[target_col].value_counts(normalize=True)
        return cond_prob

class InventoryVectorProcessor(InventoryVector):
    def __init__(self, data):
        super().__init__(data)

    def dot_product(self, vec1, vec2):
        return np.dot(vec1, vec2)

    def unit_vector(self, vec):
        norm = np.linalg.norm(vec)
        if norm != 0:
            return vec / norm if norm != 0 else vec
        else:
            raise ValueError("Zero vector cannot have a unit vector")

    def projection_vector(self, vec1, vec2):
        # project vec1 onto vec2
        v2_unit = self.unit_vector(vec2)
        scalar_proj = np.dot(vec1, v2_unit)
        return scalar_proj * v2_unit

    def angle_between(self, vec1, vec2):
        try:
            cos_theta = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            return math.degrees(math.acos(np.clip(cos_theta, -1.0, 1.0)))
        except ZeroDivisionError:
            raise ValueError("cannot compute angle between zero vectors")
        
    def check_orthogonality(self, vec1, vec2):
        return np.isclose(self.dot_product(vec1, vec2), 0.0)

    def unique_values(self, col):
        return self.data[col].unique().tolist()

    def generate_combinations(self, col, r=2):
        return list(combinations(self.unique_values(col), r))

    def generate_permutations(self, col, r=2):
        return list(permutations(self.unique_values(col), r))

# Helper function using lambda, *args, **kwargs
def summarize_column(df, col_func=lambda x: x.mean(), *args, **kwargs):
    col_name = args[0] if args else None
    subset = df[col_name] if col_name in df.columns else df
    return col_func(subset, **kwargs)

if __name__ == "__main__":
    # Simple test example
    df = pd.DataFrame({
        'VectorA': [1, 2, 3],
        'VectorB': [4, 5, 6],
        'Category': ['X', 'Y', 'Z']
    })
    p = InventoryVectorProcessor(df)
    print("Dot Product:", p.dot_product(df['VectorA'], df['VectorB']))
    print("Mean VectorA:", p.mean('VectorA'))
    print("Angle:", p.angle_between(df['VectorA'], df['VectorB']))

    # Test lambda + *args
    result = summarize_column(df, lambda x: x.sum(), 'VectorA')
    print("Summarize Column (sum VectorA):", result)
