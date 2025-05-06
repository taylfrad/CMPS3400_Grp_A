#%% MODULE BEGINS
module_name_gl = 'inventory_vector'

'''
Version: v0.4
Description:
    Parent/Child classes for vector & probability analytics,
    plus combos/permutations for categorical attributes.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-07
Date Last Updated: 2025-05-06

Doc:
    InventoryVector: basic stats, joint/conditional, array→DataFrame.
    InventoryVectorProcessor: dot/unit/projection/angle, combos/perms.
'''
#%% IMPORTS
import logging
import pandas as pd
import numpy as np
import math
from itertools import combinations, permutations

#%% CLASSES
class InventoryVector:
    def __init__(self, data: pd.DataFrame):
        logging.info("InventoryVector.__init__")
        self._data = data

    def mean(self, col: str) -> float:
        logging.info(f"mean called on {col}")
        return float(self._data[col].mean())

    def median(self, col: str) -> float:
        logging.info(f"median called on {col}")
        return float(self._data[col].median())

    def std(self, col: str) -> float:
        logging.info(f"std called on {col}")
        return float(self._data[col].std())

    def joint_counts(self, c1: str, c2: str) -> pd.Series:
        logging.info(f"joint_counts called on {c1}, {c2}")
        return self._data.groupby([c1, c2]).size()

    def joint_probabilities(self, c1: str, c2: str) -> pd.Series:
        logging.info(f"joint_probabilities called on {c1}, {c2}")
        return self.joint_counts(c1, c2) / len(self._data)

    def conditional_probability(self, target: str, given: str) -> pd.Series:
        logging.info(f"conditional_probability called: {target}|{given}")
        return self._data.groupby(given)[target].value_counts(normalize=True)

    @classmethod
    def from_pickle(cls, path: str):
        df = pd.read_pickle(path)
        return cls(df)

    def array_to_df(self, arr: np.ndarray, cols=None) -> pd.DataFrame:
        logging.info("array_to_df called")
        return pd.DataFrame(arr, columns=cols)

class InventoryVectorProcessor(InventoryVector):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        logging.info("InventoryVectorProcessor.__init__")

    def dot_product(self, v1: np.ndarray, v2: np.ndarray) -> float:
        logging.info("dot_product called")
        return float(np.dot(v1, v2))

    def unit_vector(self, v: np.ndarray) -> np.ndarray:
        logging.info("unit_vector called")
        norm = np.linalg.norm(v)
        if norm == 0:
            raise ValueError("Zero vector")
        return v / norm

    def projection_vector(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        logging.info("projection_vector called")
        uv2 = self.unit_vector(v2)
        return np.dot(v1, uv2) * uv2

    def angle_between(self, v1: np.ndarray, v2: np.ndarray) -> float:
        logging.info("angle_between called")
        dot = np.dot(v1, v2)
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        if denom == 0:
            raise ValueError("Zero vector")
        cosθ = np.clip(dot/denom, -1, 1)
        return math.degrees(math.acos(cosθ))

    def check_orthogonality(self, v1: np.ndarray, v2: np.ndarray) -> bool:
        logging.info("check_orthogonality called")
        return np.isclose(self.dot_product(v1, v2), 0.0)

    def generate_combinations(self, col: str, r: int = 2) -> list:
        """
        Generate all r-length combinations of unique values in `col`.
        """
        logging.info(f"generate_combinations called on {col}, r={r}")
        vals = self._data[col].dropna().unique().tolist()
        return list(combinations(vals, r))

    def generate_permutations(self, col: str, r: int = 2) -> list:
        """
        Generate all r-length permutations of unique values in `col`.
        """
        logging.info(f"generate_permutations called on {col}, r={r}")
        vals = self._data[col].dropna().unique().tolist()
        return list(permutations(vals, r))
    
    def sorted_joint_counts(self):
        """
        Return joint_counts dict items sorted DESC by count.
        Demonstrates a lambda used as the sort key.
        """
        # self.joint_counts is a dict {(i,j): count}
        return sorted(
            self.joint_counts.items(),
            key=lambda pair: pair[1],  # lambda!!!!
            reverse=True
        )

#%% SELF-RUN
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from config import CONFIG
    import ui

    # Load pickle for testing
    vec_parent = InventoryVector.from_pickle(CONFIG.input_pickle)
    print("Joint counts sample:\n", vec_parent.joint_counts(
        vec_parent._data.columns[0], vec_parent._data.columns[1]
    ))

    vec_proc = InventoryVectorProcessor(vec_parent._data)
    # Test vector ops
    v1 = vec_parent._data.select_dtypes(include='number').iloc[:, 0].values
    v2 = vec_parent._data.select_dtypes(include='number').iloc[:, 1].values
    print("Dot product:", vec_proc.dot_product(v1, v2))
    print("Combinations:", vec_proc.generate_combinations(
        vec_parent._data.select_dtypes(include='object').columns[0]
    ))
    print("Permutations:", vec_proc.generate_permutations(
        vec_parent._data.select_dtypes(include='object').columns[0]
    ))
