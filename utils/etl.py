import functools
import numpy as np
import pandas as pd

from pathlib import Path


def resolve(path, directory):
    p = path / directory
    return p.glob("*.xlsx")


def hhmmss_to_seconds(hh_mm_ss):
    hh_mm_ss = str(hh_mm_ss)
    return functools.reduce(lambda acc, x: acc * 60 + x,
                            map(int, hh_mm_ss.split(':')))


def concat(files, save=True, name=None):
    X = pd.concat([
        pd.read_excel(f, converters={"LapTime": hhmmss_to_seconds})
        for f in files
    ])
    X = X.reset_index()

    if save:
        processed_folder = Path("./data/_processed")
        processed_folder.mkdir(parents=False, exist_ok=True)

        X.to_csv(processed_folder / "{}.csv".format(name), index=False)

    return X


def get_datasets(data_path, dataset_names, save=True):
    p = Path(data_path)

    datasets = []
    for name in dataset_names:
        files = resolve(p, name)
        datasets.append(concat(files, save, name))

    return datasets
