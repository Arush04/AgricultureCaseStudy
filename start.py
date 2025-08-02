from enum import unique
from re import I
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import ee

ee.Authenticate()
ee.Initialize(project = "earthsat")
print(ee.String("Hello").getInfo())


# mh_precipitation = pd.read_csv("data/MH_precipitation.csv")
# mh_temp = pd.read_csv("data/MH_temperature.csv")
# dates = mh_temp['date'].astype(str).tolist()
# years = [re.match(r'^(\d{4})', date).group(1) for date in dates]
# unique_years = np.unique(years)
# print(unique_years)
# print(mh_temp.head())
# mh_temp = mh_temp.drop(columns=["Unnamed: 0.1"])
# print(mh_temp.columns)
