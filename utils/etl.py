import datetime as dt
import functools
from pathlib import Path

import numpy as np
import pandas as pd


def resolve(path, directory):
    """Get all xlsx files
    
    Arguments:
        path {Pathlib path} -- main data directory
        directory {String} -- directory containing xlsx files
    
    Returns:
        All xlsx files
    """
    p = path / directory
    return p.glob("*.xlsx")


def hhmmss_to_seconds(hh_mm_ss):
    """Convert time
    
    Arguments:
        hh_mm_ss {DateTime} -- original datetime
    
    Returns:
        [str] -- Time in seconds
    """
    hh_mm_ss = str(hh_mm_ss)
    return functools.reduce(lambda acc, x: acc * 60 + x,
                            map(int, hh_mm_ss.split(':')))


def concat(files, save=True, name=None):
    """Concat all files
    
    Arguments:
        files {list} -- xlsx files
    
    Keyword Arguments:
        save {bool} -- save concatenated file (default: {True})
        name {[type]} -- filename for output (default: {None})
    
    Returns:
        [dataframe] -- concatenated file
    """
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
    """Get dataset
    
    Arguments:
        data_path {str} -- data path
        dataset_names {str} -- name of the resulting dataset
    
    Keyword Arguments:
        save {bool} -- save the dataset (default: {True})
    
    Returns:
        [DataFrame] -- output dataset
    """
    p = Path(data_path)

    datasets = []
    for name in dataset_names:
        files = resolve(p, name)
        datasets.append(concat(files, save, name))

    return datasets


def filter_dataset(dataset, timeframe, population):
    """filter dataset on timeframe and population
    
    Arguments:
        dataset {DataFrame} -- dataset to subset from
        timeframe {int} -- days past last training
        population {str} -- subset of population
    
    Returns:
        [DataFrame] -- Subset of the original dataset
    """
    upper = dataset.Date.max()
    lower = upper - dt.timedelta(days=timeframe)

    mask = (dataset.Date <= upper) & (dataset.Date >= lower)

    if population:
        mask = mask & (dataset.Position == population)

    return dataset[mask]
