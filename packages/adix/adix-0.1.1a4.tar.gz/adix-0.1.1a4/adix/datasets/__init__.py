import os
from os.path import dirname
from typing import List

import pandas as pd

def get_dataset_names() -> List[str]:

    module_path = dirname(__file__)
    files = os.listdir(module_path)
    csv_files = [f for f in files if f.endswith(".csv")]


    datasets = [os.path.splitext(f)[0] for f in csv_files]

    return datasets


def _get_dataset_path(name: str) -> str:

    # Remove suffix 'csv' and transform to lower case
    lower_name = name.lower()
    if lower_name.endswith(".csv"):
        lower_name = os.path.splitext(lower_name)[0]

    if lower_name not in get_dataset_names():
        raise ValueError(
            f"Dataset {name} is not found."
        )

    module_path = dirname(__file__)

    path = os.path.join(module_path, 'datasets', f"{lower_name}.csv")
    return path


def load_dataset(name: str) -> pd.DataFrame:
    
    path = _get_dataset_path(name)
    df = pd.read_csv(path)
    return df
