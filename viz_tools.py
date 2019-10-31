import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def counts_plot(dictionary, r=45, c='C0', h=False, title='Data Visualisation', style='ggplot'):
	"""Draw bar plot based on dictionary input.

	Dictionary keys are used as X-values - Dictionary values are used as Y-values.

	The plot can be customised with various keyword arguments.
	"""

	plt.style.use(style)
	
	if h:
		plt.barh(*zip(*dictionary.items()), color=c)
	else:
		plt.bar(*zip(*dictionary.items()), color=c)
	plt.xticks(list(dictionary.keys()), rotation=r)
	plt.title(title)
	plt.show()

def draw_network(edges):
	"""Draw a network based on supplied list of edges.
	"""

	graph = nx.Graph()

	graph.add_edges_from(edges)

	nx.draw(graph, with_labels=True)

	plt.show()
