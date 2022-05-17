#####################################
# juntar veiculos em um único dataset
#####################################

import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime

def concat_veh(df_vehicles, path, counter):
    vehicles = os.listdir(path)

    for i in vehicles:
        counter += 1
        aux = pd.read_csv(path + i)
        aux['id'] = counter
        
        df_vehicles = pd.concat([df_vehicles, aux])
    
    return df_vehicles, counter


base_dir = Path(__file__).resolve().parent.parent.parent

df_vehicles = pd.DataFrame()
counter = 0

# Juntando veiculos do sentido NB
path = os.path.join(base_dir, 'datasets/MobileCentury/NB_veh_files/')
df_vehicles, counter = concat_veh(df_vehicles, path, counter)

# Juntando veiculos do sentido SB
path = os.path.join(base_dir, 'datasets/MobileCentury/SB_veh_files/')
df_vehicles, counter = concat_veh(df_vehicles, path, counter)

#Transformando de Unix code para datetime
df_vehicles['datetime'] = [datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S') for i in df_vehicles['unix time']]

#Renomeando colunas 
df_vehicles.rename(columns={" latitude": "latitude"," longitude" : "longitude", " speed":"speed", " postmile":"postmile"}, inplace=True)

# Gerando csv
df_vehicles.to_csv("all_vehicles.csv")
