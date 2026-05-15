class Node:
    def __init__(self, state, parent, path_cost):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

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
    def remove(self):
        if self.empty(): raise Exception("empty frontier")
        min_cost_index = 0
        for i in range(len(self.frontier)):
            if self.frontier[i].path_cost < self.frontier[min_cost_index].path_cost:
                min_cost_index = i

        node = self.frontier.pop(min_cost_index)
        return node