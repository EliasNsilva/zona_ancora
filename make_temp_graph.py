##############################################
# Criação dos grafos temporais para a base MC
##############################################
import tkinter
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

base_dir = Path(__file__).resolve().parent.parent.parent

df_vehicles = pd.read_csv(os.path.join(base_dir, 'MC_grafos/all_vehicles.csv'))

df_vehicles['datetime'] = pd.to_datetime(df_vehicles['datetime'], format="%Y-%m-%d %H:%M:%S")


        # PESQUISAR POSSIVEL BIBLIOTECA PRONTA PARA FAZER ESSE CALCULO (IGRAPH)
        # EM VEZ DE USAR RANGE, FAZER UMA BUSCA OIR IDS EXISTENTES EM DF_HOUR
        # NUMERO DE ARESTAS MUITO SUPERIOR VERIFICAR A EXISTENCIA ANTES DE CRIAR


def make_graph(df_hour):
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
                    #print("veh1", loc1)
                    #print("veh2", loc2)
                    distance = hs.haversine(loc1,loc2,unit=Unit.METERS)
                    if distance <= 100.00:
                        #print(f"distancia entre {j} e {l} = {distance}")
                        graph.add_edge(j,l)
                        break
    #print(summary(graph))
    fig, ax = plt.subplots()
    plot(graph, target= ax)
    plt.show()


df_hour = df_vehicles.loc[df_vehicles['datetime'].dt.hour == 0]
make_graph(df_hour[df_hour['id'] < 50])
    
for i in range(0,24):
    df_hour = df_vehicles.loc[df_vehicles['datetime'].dt.hour == i]
    #make_graph(df_hour[df_hour['id'] < 100])
    if not df_hour.empty:
        pass
        # criar um grafo
        # for j in range(min(df_hour['id']), max(df_hour['id'])):
            # df_an_veh = df_hour[df_hour[id] == j]
            # if df_an_veh.empty:
                # pass
            # for k in df_an_veh:
                # k.lt 
                # k.lg
                # for l in range(j + 1, max(df_hour['id'])):
                    # df_veh = df_hour[df_hour[id] == l]
                    # if df_veh.empty:
                        # pass
                    # for m in df_veh:
                        # distance = (k.lt, k.lg) (m.lt, m.lg)
                        # if distance >= 100:
                            # creat edge(j,l)
                            # breack


# loc1 = (df_vehicles['latitude'][0], df_vehicles['longitude'][0])
# loc2 = (df_vehicles['latitude'][1], df_vehicles['longitude'][1])
# print(loc1[0])

# # loc1 = (37.531738571,-122.005581047)
# # loc2 = (37.531850051,-122.005789924)

# print(hs.haversine(loc1,loc2,unit=Unit.METERS))
