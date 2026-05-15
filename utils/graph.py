from structs import *
from unicodedata import normalize
from pathlib import Path
import csv
import sys

names = {} #mapear nome para ids correspondentes
municipios = {}
test = "--test" in sys.argv

BASE_DIR = Path(__file__).resolve().parent.parent
if test: DATA_PATH = BASE_DIR / "data" / "municipios_teste.csv"
else: DATA_PATH = BASE_DIR / "data" / "municipios_final.csv"

with open(DATA_PATH, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

    for row in rows:
        id = row["id"]
        name =  normalize('NFKD', row["name"]).encode('ASCII', 'ignore').decode('ASCII')

        municipios[id] = {"name": name, "neighbors": []}

        if name.lower() not in names: names[name.lower()] = id
        else: names[name.lower()].add(id)

    for row in rows:
        neighbors_distance = []
        for neighbor in row["neighbors"].split(','):
            if ":" not in neighbor: continue
            name, distance = neighbor.split(':')
            name = name.strip().lower()
            name = normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
            if name in names: neighbors_distance.append((names[name], float(distance)))
        municipios[row["id"]]["neighbors"] = neighbors_distance


def main():
    source = input("Município: ").lower().strip()
    source = normalize('NFKD', source).encode('ASCII', 'ignore').decode('ASCII')
    source = municipio_id_for_name(source)
    if source is None: sys.exit("Not found.")

    target = input("Município: ").lower().strip()
    target = normalize('NFKD', target).encode('ASCII', 'ignore').decode('ASCII')
    target = municipio_id_for_name(target)
    if target is None: sys.exit("Not found.")

    path, cost = smaller_separation_degree_path(source, target)

    if path is None: print("Not connected.")
    else:
        degrees = len(path)
        print(f"Minimum of {degrees} municipios of separation if:")
        path = [(None, source)] + path
        for i in range(degrees):
            municipio1 = municipios[path[i][1]]["name"]
            municipio2 = municipios[path[i + 1][1]]["name"]
            print(f"go from {municipio1} to {municipio2}", end=' ')
        print(f"\n{cost}km of separation")

def smaller_separation_degree_path(source, target):
    explored = set()
    start = Node(state=source, parent=None, path_cost=0)
    frontier = QueueFrontier()
    frontier.add(start)
    while True:
        if frontier.empty(): return None, None
        node = frontier.remove()
        if node.state == target:
            cost = node.path_cost
            solution = []
            while node.parent is not None:
                solution.append((node.parent, node.state))
                node = node.parent
            solution.reverse()
            return solution, cost
        explored.add(node.state)
        for neighbor, distance in municipios[node.state]["neighbors"]:
            if not frontier.contains_state(neighbor) and neighbor not in explored:
                child = Node(state=neighbor, parent=node, path_cost=node.path_cost + distance)
                frontier.add(child)

def municipio_id_for_name(name):
    municipio_id = names.get(name.lower())
    if len(municipio_id) == 0: return None
    else: return municipio_id

main()
