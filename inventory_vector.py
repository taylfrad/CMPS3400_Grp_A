# inventory_vector.py
#%% MODULE BEGINS
module_name_gl = 'inventory_vector'

'''
Version: v0.5
Description:
    Parent/Child classes for vector & probability analytics,
    plus combos/permutations for categorical attributes.
Authors:
    Taylor Fradella, Angel Njoku
Date Created     : 2025-04-07
Date Last Updated: 2025-05-06

Doc:
    InventoryVector: basic stats, joint/conditional, array→DataFrame.
    InventoryVectorProcessor: dot/unit/projection/angle, combos/perms,
      plus a self-run display of every required metric.
'''
#%% IMPORTS
import logging
import os
import pandas as pd
import numpy as np
import math
from itertools import combinations, permutations

from config import CONFIG
import ui

#%% CLASSES
class InventoryVector:
    def __init__(self, data: pd.DataFrame):
        logging.info("InventoryVector.__init__")
        self._data = data

    def mean(self, col: str) -> float:
        return float(self._data[col].mean())

    def median(self, col: str) -> float:
        return float(self._data[col].median())

    def std(self, col: str) -> float:
        return float(self._data[col].std())

    def joint_counts(self, c1: str, c2: str) -> pd.Series:
        return self._data.groupby([c1, c2]).size()

    def joint_probabilities(self, c1: str, c2: str) -> pd.Series:
        return self.joint_counts(c1, c2) / len(self._data)

    def conditional_probability(self, target: str, given: str) -> pd.Series:
        return self._data.groupby(given)[target].value_counts(normalize=True)

    @classmethod
    def from_pickle(cls, path: str):
        df = pd.read_pickle(path)
        return cls(df)

    def array_to_df(self, arr: np.ndarray, cols=None) -> pd.DataFrame:
        return pd.DataFrame(arr, columns=cols)


class InventoryVectorProcessor(InventoryVector):
    def __init__(self, data: pd.DataFrame):
        super().__init__(data)
        logging.info("InventoryVectorProcessor.__init__")

    def dot_product(self, v1: np.ndarray, v2: np.ndarray) -> float:
        return float(np.dot(v1, v2))

    def unit_vector(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        if norm == 0:
            raise ValueError("Zero vector")
        return v / norm

    def projection_vector(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        uv2 = self.unit_vector(v2)
        return np.dot(v1, uv2) * uv2

    def angle_between(self, v1: np.ndarray, v2: np.ndarray) -> float:
        dot = np.dot(v1, v2)
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        cosθ = np.clip(dot/denom, -1, 1)
        return math.degrees(math.acos(cosθ))

    def check_orthogonality(self, v1: np.ndarray, v2: np.ndarray) -> bool:
        return np.isclose(self.dot_product(v1, v2), 0.0)

    def generate_combinations(self, col: str, r: int = 2) -> list:
        vals = self._data[col].dropna().unique().tolist()
        return list(combinations(vals, r))

    def generate_permutations(self, col: str, r: int = 2) -> list:
        vals = self._data[col].dropna().unique().tolist()
        return list(permutations(vals, r))

    def process_and_display(self):
        # Identify numeric & categorical columns
        num_cols = self._data.select_dtypes(include='number').columns.tolist()
        cat_cols = self._data.select_dtypes(include=['object']).columns.tolist()
        c1, c2 = num_cols[:2]

        # Joint counts & probabilities
        print("\n------------------------------------------------------------", flush=True)
        print("                   Joint Counts", flush=True)
        print("------------------------------------------------------------", flush=True)
        jc = self.joint_counts(c1, c2)
        for (a, b), cnt in jc.items():
            print(f"({a}, {b}): {cnt}", flush=True)

        print("\n------------------------------------------------------------", flush=True)
        print("               Joint Probabilities", flush=True)
        print("------------------------------------------------------------", flush=True)
        jp = self.joint_probabilities(c1, c2)
        for (a, b), p in jp.items():
            print(f"({a}, {b}): {p:.2f}", flush=True)

        print("\n------------------------------------------------------------", flush=True)
        print("           Conditional Probabilities", flush=True)
        print("------------------------------------------------------------", flush=True)
        cp = self.conditional_probability(c1, c2)
        for (given_val, target_val), p in cp.items():
            print(f"P({target_val}|{given_val}) = {p:.2f}", flush=True)

        # Vector operations
        v1 = self._data[c1].values
        v2 = self._data[c2].values

        print("\n------------------------------------------------------------", flush=True)
        print("                 Vector Operations", flush=True)
        print("------------------------------------------------------------", flush=True)
        print(f"Position Vector {c1}: {v1.tolist()}", flush=True)
        print(f"Position Vector {c2}: {v2.tolist()}", flush=True)

        uv1 = self.unit_vector(v1)
        uv2 = self.unit_vector(v2)
        print(f"Unit Vector {c1}    : {uv1.tolist()}", flush=True)
        print(f"Unit Vector {c2}    : {uv2.tolist()}", flush=True)

        proj = self.projection_vector(v1, v2)
        print(f"Projection {c1}→{c2} : {proj.tolist()}", flush=True)

        dp = self.dot_product(v1, v2)
        ang = self.angle_between(v1, v2)
        ortho = self.check_orthogonality(v1, v2)
        print(f"Dot Product: {dp}", flush=True)
        print(f"Angle (deg): {ang:.2f}", flush=True)
        print(f"Orthogonal?: {ortho}", flush=True)

        # Combinations & Permutations
        if cat_cols:
            cat = cat_cols[0]
            combs = self.generate_combinations(cat)
            perms = self.generate_permutations(cat)

            print("\n------------------------------------------------------------", flush=True)
            print("                   Combinations", flush=True)
            print("------------------------------------------------------------", flush=True)
            print(f"{cat}: {combs}", flush=True)

            print("\n------------------------------------------------------------", flush=True)
            print("                   Permutations", flush=True)
            print("------------------------------------------------------------", flush=True)
            print(f"{cat}: {perms}", flush=True)

            # export to CSV
            df_c = pd.DataFrame(combs, columns=[f"{cat}1", f"{cat}2"])
            df_p = pd.DataFrame(perms, columns=[f"{cat}1", f"{cat}2"])
            df_c.to_csv(os.path.join(CONFIG.output_dir, f"{cat}_combinations.csv"), index=False)
            df_p.to_csv(os.path.join(CONFIG.output_dir, f"{cat}_permutations.csv"), index=False)
            logging.info("Exported combinations & permutations CSVs")

        else:
            print("\nNo categorical column found for combos/perms.", flush=True)


#%% SELF-RUN
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    vec_parent = InventoryVector.from_pickle(CONFIG.input_pickle)
    InventoryVectorProcessor(vec_parent._data).process_and_display()
