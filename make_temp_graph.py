##############################################
# Criação dos grafos temporais para a base MC
##############################################
#import tkinter
import matplotlib
#matplotlib.use("tkAgg")

import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from igraph import *
import haversine as hs
from haversine import Unit
import os
from pathlib import Path
import datetime

base_dir = Path(__file__).resolve().parent.parent.parent

df_vehicles = pd.read_csv(os.path.join(base_dir, 'MC_grafos/all_vehicles.csv'))

df_vehicles['datetime'] = pd.to_datetime(df_vehicles['datetime'], format="%Y-%m-%d %H:%M:%S")


# PESQUISAR POSSIVEL BIBLIOTECA PRONTA PARA FAZER ESSE CALCULO (IGRAPH)
# EM VEZ DE USAR RANGE, FAZER UMA BUSCA OIR IDS EXISTENTES EM DF_HOUR
# NUMERO DE ARESTAS MUITO SUPERIOR VERIFICAR A EXISTENCIA ANTES DE CRIAR


def make_graph(df_hour, file):
    # criar um grafo
    graph = Graph()

    vehicles = df_hour['id'].unique()

    graph.add_vertices(len(vehicles))
    # for i in graph.vs:
    #     print("vertices", i)
    for j in range(len(vehicles)):
        print("veh",j)
        print("graph",summary(graph))

        df_an_veh = df_hour[df_hour['id'] == vehicles[j]]

        if df_an_veh.empty:
            print("oxe")
            pass

        for index, row in df_an_veh.iterrows():
            lat_veh1 = row.latitude
            long_veh1 = row.longitude
            p = row. postmile

            for l in range(j+1, len(vehicles)):
                #print("other veh",l)
                if graph.are_connected(j, l):
                    continue

                df_veh = df_hour[df_hour['id'] == vehicles[l]]
                if df_veh.empty:
                    continue
                for index, row in df_veh.iterrows():
                    # distance = (k.lt, k.lg) (m.lt, m.lg)
                    lat_veh2 = row.latitude
                    long_veh2 = row.longitude
                    loc1 = (lat_veh1, long_veh1)
                    loc2 = (lat_veh2, long_veh2)

                    #print(f"post v1 {p} posnt v2 {row.postmile}")
                    #print("veh1", loc1)
                    #print("veh2", loc2)
                    distance = hs.haversine(loc1,loc2,unit=Unit.METERS)
                    if distance <= 100.00:
                        #print(f"distancia entre {j} e {l} = {distance}")
                        graph.add_edge(j,l)
                        
                        file.write(f"{vehicles[j]}, {vehicles[l]}\n")
                        break
    #print(summary(graph))
    # fig, ax = plt.subplots()
    # plot(graph, target= ax)
    # plt.show()


    
for i in range(0,24):
    df_hour = df_vehicles.loc[df_vehicles['datetime'].dt.hour == i]

    if not df_hour.empty:
        for j in range(4):
            file = open(f"graph_hour({i})_{j}.txt", "a+")

            min_date = min(df_hour['datetime'])
            max_date = min_date + datetime.timedelta(minutes=15)

            print("max",max(df_hour['datetime']))

            if max_date > max(df_hour['datetime']):
                max_date = max(df_hour['datetime'])
                j = 5
            else:
                df_hour = df_hour[df_hour['datetime'] > max_date]

            print(min_date,max_date)

            make_graph(df_hour[df_hour['datetime'] <= max_date], file)

            file.close()


