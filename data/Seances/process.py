import numpy as np
import pandas as pd

dataset = pd.read_excel("./20200206.xlsx")
ind = dataset[dataset.Nom.astype(str).str.isdigit()].index
dataset = dataset.drop(ind)

dataset.to_excel("./20200206.xlsx", index=False)
