import csv
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

            if name.lower() not in names: names[name.lower()] = id

        for row in rows:
            neighbors_distance = []
            for neighbor in row["neighbors"].split(','):
                if ":" not in neighbor: continue
                name, distance = neighbor.split(':')
                name = name.strip().lower()
                name = normalize_name(name)
                if name in names: neighbors_distance.append((names[name], float(distance)))
            municipios[row["id"]]["neighbors"] = neighbors_distance
    return names, municipios

def normalize_name(name):
    return normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')