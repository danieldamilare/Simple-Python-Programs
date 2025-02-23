import time
import random
import statistics
from collections import deque

class Node:
    def __init__(self, name):
        self.name = name
    def get_name(self):
        return self.name
    def __str__(self):
        return self.name


class Edge:
    def __init__(self, src: Node, dest: Node):
        self.src = src
        self.dest = dest
    def get_source(self):
        return self.src
    def get_destination(self):
        return self.dest

    def __str__(self):
        return self.src.get_name() + '->' + self.dest.get_name()


class Graph:
    def __init__(self):
        self.edges = {}

    def add_node(self, node: Node):
        if node in self.edges:
            raise ValueError("Duplicate node")
        self.edges[node] = []

    def add_edge(self, edge:Edge):
        if not (edge.get_source() in self.edges and edge.get_destination() in self.edges):
            raise ValueError("Node missing in graph")
        self.edges[edge.get_source()].append(edge.get_destination())

    def children_of(self, node: Node):
        return self.edges[node]

    def get_node(self, name):
        # print("In get node")
        for n in self.edges:
            # print(n)
            # print("n edges: ", self.edges[n])
            if n.get_name() == name:
                return n
        raise NameError(name)

    def has_node(self, node):
        return node in self.edges

    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result += src.get_name() + '->' + dest.get_name() + '\n'
        return result[:-1]

def make_graph(*args) -> Graph: #accept a tuple of edges in a graph and build the
    return_graph = Graph()
    nodes = {}

    for src_name, dst_name in args:
        if src_name not in nodes:
            nodes[src_name] = Node(src_name)
        if dst_name not in nodes:
            nodes[dst_name] = Node(dst_name)

        if not return_graph.has_node(nodes[src_name]):
            return_graph.add_node(nodes[src_name])

        if not return_graph.has_node(nodes[dst_name]):
            return_graph.add_node(nodes[dst_name])

        return_graph.add_edge(Edge(nodes[src_name], nodes[dst_name]))

    return return_graph

def build_graph():
    return_graph = make_graph(('Boston', 'Providence'), ('Boston', "New York"), 
               ('Providence', 'Boston'), ('Providence', 'New York'),
               ('New York', 'Chicago'), ('Chicago', 'Denver'),
               ('Denver', 'Phoenix'), ('Denver', 'New York'),
               ('Los Angeles', 'Boston'))
    return return_graph

def bfs_shortest_path(graph: Graph, start: Node, dest: Node):
    initial_path = [start]
    path_queue = deque([initial_path])
    found = False
    while (len(path_queue) > 0):
        current_path = path_queue.popleft()
        # print(f"Current path: {[x.get_name() for x in current_path]}")
        if current_path[-1] == dest:
            found = True
            break
        else:
            for node in graph.children_of(current_path[-1]):
                if node not in current_path:
                    path_queue.append(current_path + [node])
    return current_path if found else None

def dfs_shortest_path(graph: Graph,
                      start: Node,
                      dest: Node,
                      path: set = None,
                      memo: dict = None) -> list:

    if path is None:
        path = set()
    if memo is None:
        memo = {}

    if start == dest:
        return [start]
    key = start, dest
    if key in memo:
        return memo[key]

    path.add(start)
    shortest = None

    for node in graph.edges[start]:
        if node in path:  # Skip if would create cycle
            continue

        new_path = dfs_shortest_path(graph, node, dest, path, memo)
        if new_path is None:
            continue

        candidate = [start] + new_path
        if shortest is None or len(candidate) < len(shortest):
            shortest = candidate

    memo[key] = shortest

    path.remove(start)
    return shortest

def generate_large_graph(num_nodes: int, edge_density: float) -> Graph:
    """Generate a larger random graph for testing."""
    g = Graph()
    # Create nodes
    nodes = [Node(str(i)) for i in range(num_nodes)]
    for node in nodes:
        g.add_node(node)

    # Add random edges
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_density:
                g.add_edge(Edge(nodes[i], nodes[j]))
    return g, nodes

def benchmark_pathfinding(graph: Graph, nodes: list, num_trials: int = 100):
    """Run multiple pathfinding trials and collect statistics."""
    bfs_times = []
    dfs_times = []

    for _ in range(num_trials):
        # Select random start and end nodes
        start = random.choice(nodes)
        end = random.choice(nodes)

        # Time BFS
        start_time = time.perf_counter()  # More precise than time.time()
        bfs_path = bfs_shortest_path(graph, start, end)
        bfs_times.append(time.perf_counter() - start_time)

        # Time DFS
        start_time = time.perf_counter()
        dfs_path = dfs_shortest_path(graph, start, end)
        dfs_times.append(time.perf_counter() - start_time)
        if (bfs_path is not None and dfs_path is not None) and len(bfs_path) != len(dfs_path):
            print([x.get_name() for x in dfs_path])
            print([x.get_name() for x in bfs_path])
            for i in range(len(bfs_path) -1):
                if (bfs_path[i+1] not in graph.children_of(bfs_path[i])):
                    print(f"Incorrect path: {bfs_path[i].get_name()} -> {bfs_path[i+1].get_name()}")
            for i in range(len(dfs_path) - 1):
                if (dfs_path[i+1] not in graph.children_of(dfs_path[i])):
                    print(f"Incorrect path: {dfs_path[i].get_name()} -> {dfs_path[i+1].get_name()}")
            raise Exception("Code error")

    return {
        'bfs': {
            'mean': statistics.mean(bfs_times),
            'median': statistics.median(bfs_times),
            'std_dev': statistics.stdev(bfs_times)
        },
        'dfs': {
            'mean': statistics.mean(dfs_times),
            'median': statistics.median(dfs_times),
            'std_dev': statistics.stdev(dfs_times)
        }
    }


if __name__ == '__main__':
    # graph = build_graph()
    # print(graph)
    # print('\n\n')
    # start = graph.get_node('Boston')
    # end = graph.get_node('Phoenix')
    # print("start, end", start, end, "\n\n")
    # start_time = time.time()
    # path = bfs_shortest_path(graph, start, end)
    # bfs_time_used = time.time() - start_time
    # if (path is None):
    #     print(f"No path between {start.get_name()} to {end.get_name()}")
    # else:
    #     print(' -> '.join(x.get_name() for x in path))

    # start_time = time.time()
    # path = dfs_shortest_path(graph, start, end)
    # dfs_time_used = time.time() - start_time
    # if (path is None):
    #     print(f"No path between {start.get_name()} to {end.get_name()}")
    # else:
    #     print(' -> '.join(x.get_name() for x in path))

    # print(f"Bfs time used: {bfs_time_used}")
    # print(f"Dfs time used: {dfs_time_used}")

       for size in [10, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]:
        print(f"\nTesting with graph size: {size}")
        graph, nodes = generate_large_graph(size, edge_density=0.2)
        results = benchmark_pathfinding(graph, nodes, num_trials=100)

        print(f"BFS Results:")
        print(f"  Mean time:   {results['bfs']['mean']*1000:.3f}ms")
        print(f"  Median time: {results['bfs']['median']*1000:.3f}ms")
        print(f"  Std Dev:     {results['bfs']['std_dev']*1000:.3f}ms")

        print(f"\nDFS Results:")
        print(f"  Mean time:   {results['dfs']['mean']*1000:.3f}ms")
        print(f"  Median time: {results['dfs']['median']*1000:.3f}ms")
        print(f"  Std Dev:     {results['dfs']['std_dev']*1000:.3f}ms")
