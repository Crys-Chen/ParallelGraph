import networkx as nx
import matplotlib.pyplot as plt 
from inst import *

def build_graph(insts: "list[Instruction]"):
    graph = nx.Graph()
    for i, inst in enumerate(insts):
        graph.add_node(inst.step)
        for pre in list(inst.previous):
            assert graph.has_node(pre)
            graph.add_edge(pre, inst.step)
        # plt.clf()
        # nx.draw(graph, with_labels=True)
        # plt.savefig("graphs/"+str(i)+".png")
        subgraphs = []
        for sub in nx.connected_components(graph):
            subgraphs.append(graph.subgraph(sub))

        print(len(subgraphs))

