from structs import *
from unicodedata import normalize
import csv
import sys

names = {} #mapear nome para um set de ids correspondentes
municipios = {}

with open(f"../data/municipios.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

    for row in rows:
        id = row["id"]
        name =  normalize('NFKD', row["name"]).encode('ASCII', 'ignore').decode('ASCII')

        municipios[id] = {"name": name,
                          "neighbors": set()}

        if name.lower() not in names: names[name.lower()] = {id}
        else: names[name.lower()].add(id)

    for row in rows:
        for neighbor in row["neighbors"].split(','):
            name = neighbor.strip().lower()
            name = normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
            if name in names: municipios[row["id"]]["neighbors"].update(names[name])

def main():
    source = input("Município: ").lower().strip()
    source = normalize('NFKD', source).encode('ASCII', 'ignore').decode('ASCII')
    source = municipio_id_for_name(source)
    if source is None: sys.exit("Not found.")

    target = input("Município: ").lower().strip()
    target = normalize('NFKD', target).encode('ASCII', 'ignore').decode('ASCII')
    target = municipio_id_for_name(target)
    if target is None: sys.exit("Not found.")

    path = shortest_path(source, target)

    if path is None: print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} municípios of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            municipio1 = municipios[path[i][1]]["name"]
            municipio2 = municipios[path[i + 1][1]]["name"]
            print(f"{i + 1}: go from {municipio1} to {municipio2}")

def shortest_path(source, target):
    explored = set()
    start = Node(state=source, parent=None, path_cost=0)
    frontier = QueueFrontier()
    frontier.add(start)
    while True:
        if frontier.empty(): return None
        node = frontier.remove()
        if node.state == target:
            solution = []
            while node.parent is not None:
                solution.append((node.parent, node.state))
                node = node.parent
            solution.reverse()
            return solution
        explored.add(node.state)
        for neighbor in municipios[node.state]["neighbors"]:
            if not frontier.contains_state(neighbor) and neighbor not in explored:
                child = Node(state=neighbor, parent=node, path_cost=0)
                frontier.add(child)

def municipio_id_for_name(name):
    municipio_id = list(names.get(name.lower(), set()))
    if len(municipio_id) == 0: return None
    elif len(municipio_id) > 1:
        print(f"Which '{name}'?")
        for id in municipio_id:
            municipio = municipios[id]
            name = municipio["name"]
            print(f"ID: {id}, Name: {name}")
        try:
            id = input("Intended Person ID: ")
            if id in municipio_id: return id
        except ValueError: pass
        return None
    else: return municipio_id[0]

main()
