##############################################
# Criação dos grafos temporais para a base MC
##############################################

import pandas as pd
import numpy as np
from igraph import *
import haversine as hs
from haversine import Unit
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent.parent

df_vehicles = pd.read_csv(os.path.join(base_dir, 'MC_grafos/all_vehicles.csv'))

df_vehicles['datetime'] = pd.to_datetime(df_vehicles['datetime'], format="%Y-%m-%d %H:%M:%S")


for i in range(0,24):
    df_hour = df_vehicles.loc[df_vehicles['datetime'].dt.hour == i]

    if not df_hour.empty:


# loc1 = (df_vehicles['latitude'][0], df_vehicles['longitude'][0])
# loc2 = (df_vehicles['latitude'][1], df_vehicles['longitude'][1])
# print(loc1[0])

# # loc1 = (37.531738571,-122.005581047)
# # loc2 = (37.531850051,-122.005789924)

# print(hs.haversine(loc1,loc2,unit=Unit.METERS))
