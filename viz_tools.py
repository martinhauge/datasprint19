import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def counts_plot(dictionary, r=45, c='C0', size=(8, 6), horizontal=False, title='Data Visualisation', style='ggplot'):
    """Draw bar plot based on dictionary input.

    Dictionary keys are used as X-values - Dictionary values are used as Y-values.

    The plot can be customised with various keyword arguments.
    """

    plt.style.use(style)
    
    plt.figure(figsize=size)
    
    if horizontal:
        dictionary = dict(sorted(dictionary.items(), key=(lambda x: x[1]), reverse=False))
        plt.barh(*zip(*dictionary.items()), color=c)
    else:
        plt.bar(*zip(*dictionary.items()), color=c)
        plt.xticks(list(dictionary.keys()), rotation=r)
    plt.title(title)
    plt.show()

def draw_network(edges, node_col='#1f78b4', edge_col='k'):
    """Draw a network based on supplied list of edges.
    """

    graph = nx.Graph()

    graph.add_edges_from(edges)

    nx.draw(graph, with_labels=True, node_color=node_col, edge_color=edge_col)

    plt.show()
