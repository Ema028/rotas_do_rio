from pathlib import Path
import sys
try:
    from structs import *
    from load_data import *
except ModuleNotFoundError:
    from src.structs import *
    from src.load_data import *

test = "--test" in sys.argv

BASE_DIR = Path(__file__).resolve().parent.parent
if test: DATA_PATH = BASE_DIR / "data" / "municipios_teste.csv"
else: DATA_PATH = BASE_DIR / "data" / "municipios_final.csv"

names, municipios = load_data(DATA_PATH)

def main():
    source = input("Município: ").lower().strip()
    source = normalize_name(source)
    source = municipio_id_for_name(source)
    if source is None: sys.exit("Not found.")

    target = input("Município: ").lower().strip()
    target = normalize_name(target)
    target = municipio_id_for_name(target)
    if target is None: sys.exit("Not found.")

    path, cost = shortest_path(source, target, strategy='min_degrees')

    if path is None: print("Not connected.")
    else:
        print(f"Minimum of {len(path)} municipios of separation if:")
        print_path(path)
        print(f"Total of {cost:.2f}km of separation\n")

    path, cost = shortest_path(source, target)
    if path is None: pass
    else:
        print(f"Minimum of {cost:.2f}km of separation if:")
        print_path(path)
        print(f"Total of {len(path)} municipios of separation")

def print_path(path):
    last_index = len(path) - 1
    for i in range(last_index):
        municipio1 = municipios[path[i][1]]["name"]
        municipio2 = municipios[path[i + 1][1]]["name"]
        print(f"go from {municipio1} to {municipio2}", end=' ')
        if i < last_index - 1: print("->", end=' ')
        else: print("")

def shortest_path(source, target, strategy='less_distance'):
    explored = set()
    start = Node(state=source, parent=None, path_cost=0)
    if strategy == 'min_degrees': frontier = QueueFrontier()
    else: frontier = PriorityFrontier()
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
            return [(None, source)] + solution, cost
        explored.add(node.state)
        for neighbor, distance in municipios[node.state]["neighbors"]:
            if not frontier.contains_state(neighbor) and neighbor not in explored:
                child = Node(state=neighbor, parent=node, path_cost=node.path_cost + distance)
                frontier.add(child)

def municipio_id_for_name(name):
    municipio_id = names.get(name.lower())
    if not municipio_id: return None
    else: return municipio_id

if __name__ == "__main__":
    main()