import networkx as nx
import matplotlib.pyplot as plt
from typing import List
from ..core.entities import CodeEntity

class CallGraphVisualizer:
    def __init__(self, entities: List[CodeEntity]):
        self.entities = entities
        self.graph = nx.DiGraph()

    def build_graph(self):
        for entity in self.entities:
            self.graph.add_node(entity.name)
            for callee in entity.calls:
                self.graph.add_edge(entity.name, callee)

    def draw(self, output_path: str = None):
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10, arrows=True)

        if output_path:
            plt.savefig(output_path, format='png')
        else:
            plt.show()

    def export_as_dot(self, dot_path: str):
        nx.drawing.nx_pydot.write_dot(self.graph, dot_path)
``