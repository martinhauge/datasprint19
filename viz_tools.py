import pandas as pd
import matplotlib.pyplot as plt


def dict_plot(dictionary, r=45, title='Dictionary Plot', style='ggplot'):
	plt.style.use(style)
	plt.bar(*zip(*dictionary.items()))
	plt.xticks(list(dictionary.keys()), rotation=r)
	plt.title(title)
