from heuristic import heuristic_haversine
from pathlib import Path
from load_data import load_coordinates

BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "coordinates.json"

coordinates = load_coordinates(DATA_PATH)

class Node:
    def __init__(self, state, parent, path_cost):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.estimated_cost = None

class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty(): raise Exception("empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


class PriorityFrontier(QueueFrontier):
    def add(self, node):
        self.frontier.append(node)
        self.frontier.sort(key=lambda x: x.path_cost, reverse=True)

    def remove(self):
        if self.empty(): raise Exception("empty frontier")
        return self.frontier.pop()


class AstarFrontier(PriorityFrontier):
    def __init__(self, target, coordinates=coordinates, heuristic=heuristic_haversine):
        super().__init__()
        self.target = target
        self.coordinates = coordinates
        self.heuristic = heuristic

    def add(self, node):
        g = node.path_cost
        h = self.heuristic(node.state, self.target, self.coordinates)
        node.priority_cost = g + h

        self.frontier.append(node)
        self.frontier.sort(key=lambda x: x.priority_cost, reverse=True)