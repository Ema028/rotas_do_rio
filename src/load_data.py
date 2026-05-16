import csv
import os
import inspect
import streamlit as st
from unicodedata import normalize

def load_data(DATA_PATH):
    names = {}  # mapear nome para ids correspondentes
    municipios = {}

    with open(DATA_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

        for row in rows:
            id = row["id"]
            name = normalize_name(row["name"])

            municipios[id] = {"name": name, "neighbors": []}

            if name not in names: names[name.lower()] = id

        for row in rows:
            neighbors_distance = []
            for neighbor in row["neighbors"].split(','):
                if ":" not in neighbor: continue
                name, distance = neighbor.split(':')
                name = normalize_name(name)
                if name in names: neighbors_distance.append((names[name], float(distance)))
            municipios[row["id"]]["neighbors"] = neighbors_distance
    return names, municipios

def normalize_name(name):
    return normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII').lower().strip()

def log(*args, print=print, **kwargs):
    stack = inspect.stack() #historico arquivos rodando agr
    in_streamlit = any("app.py" in os.path.basename(frame.filename) for frame in stack)

    if in_streamlit: st.write(*args, **kwargs)
    else: print( *args, **kwargs)