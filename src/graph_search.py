import time
import sys
try:
    from structs import *
    from load_data import *
except ModuleNotFoundError:
    from src.structs import *
    from src.load_data import *

test = "--test" in sys.argv
print = log

BASE_DIR = Path(__file__).resolve().parent.parent
if test: DATA_PATH = BASE_DIR / "data" / "municipios_teste.csv"
else:    DATA_PATH = BASE_DIR / "data" / "municipios_final.csv"

names, municipios = load_data(DATA_PATH)

def main():
    source = input("Município: ")
    source = normalize_name(source)
    source = municipio_id_for_name(source)
    if source is None: sys.exit("Not found.")

    target = input("Município: ")
    target = normalize_name(target)
    target = municipio_id_for_name(target)
    if target is None: sys.exit("Not found.")

    print_all(source, target)

def print_path(path, cost, explored):
    print(f"{len(path)} municípios de separação | {cost:.2f}km de distância | {explored} nós explorados")
    path_names = []
    for _, id_atual in path:
        path_names.append(municipios[id_atual]["name"])
    print(" ➔ ".join(path_names))

def print_all(source, target):
    estrategias = [('min_degrees', 'Busca em Largura (BFS - Menos Municípios)'),
                   ('less_distance', 'Custo Uniforme (Dijkstra - Menor Quilometragem)'),
                   ('a_star', 'Algoritmo A* (Busca Otimizada com Heurística)')]
    for estrategia, descricao in estrategias:
        print(f"## {descricao}")
        tempo_inicio = time.perf_counter()
        path, cost, explored = shortest_path(source, target, strategy=estrategia)
        tempo_fim = time.perf_counter()
        tempo_total = (tempo_fim - tempo_inicio) * 1000

        if path is None: print(f"Não conectados. **Tempo de execução**: {tempo_total:.5f} ms | **Nós explorados**: {explored}")
        else:            print_path(path, cost, explored); print(f"**Tempo de execução**: {tempo_total:.5f} ms")

def shortest_path(source, target, strategy='a_star'):
    explored = set()
    start = Node(state=source, parent=None, path_cost=0)
    if   strategy == 'min_degrees'  : frontier = QueueFrontier()
    elif strategy == 'less_distance': frontier = PriorityFrontier()
    else:                             frontier = AstarFrontier(target)
    frontier.add(start)
    while True:
        if frontier.empty(): return None, None, None
        node = frontier.remove()
        if node.state == target:
            cost = node.path_cost
            solution = []
            while node.parent is not None:
                solution.append((node.parent, node.state))
                node = node.parent
            solution.reverse()
            return [(None, source)] + solution, cost, len(explored)
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