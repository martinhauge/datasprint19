import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def dict_plot(dictionary, r=45, c='C0', title='Dictionary Plot', style='ggplot'):
	plt.style.use(style)
	plt.bar(*zip(*dictionary.items()), color=c)
	plt.xticks(list(dictionary.keys()), rotation=r)
	plt.title(title)

def draw_network(edges):
	"""Draw a network based on supplied list of edges.
	"""

	graph = nx.Graph()

	graph.add_edges_from(edges)

	nx.draw(graph, with_labels=True)

	plt.show()
