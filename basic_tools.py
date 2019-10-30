import pandas as pd
from helpers import frame_check

def counter(df, col, sep=';', drop_na=True, na_value='N/A', sort='values', top=None, min_val=None):
	"""Return dictionary of value counts.

	Count and sort values of specified column in DataFrame.
	
	Parameters
	----------
	df : DataFrame
		The DataFrame to analyse.
	col : str
		Name of column to count.
	sep : str, default ';'
		Value of separator for parsing multi-value cells.
	drop_na : bool, default True
		Exclude NA values from counting.
	na_value : str, default 'N/A'
		NA value to use when "drop_na=False".
	sort : {'values', 'keys'}, default 'values'
		Sort the dictionary by values or keys.
	top : int, default None, optional
		Limit the dictionary by specifying the number of items to include in descending order.
	min_val : int, default None, optional
		Specify the minimum number of occurences to include in dictionary.
	"""
	
	frame_check(df, col)

	count_dict = dict()

	# Handle NA values before counting.
	if drop_na:
		df = df.dropna(axis=0, subset=[col])
	else:
		df = df.fillna(value=na_value)

	# Iterate over cells in column and count values.
	for row in df.index:
		for item in df[col][row].split(sep):
			item = item.strip()
			if item in count_dict:
				count_dict[item] += 1
			else:
				count_dict[item] = 1

	# Sort dictionary by keys or values
	if not sort in ['keys', 'values']:
		print('Sort method not recognised. Must be "keys" or "values". Default sorting by values.')
		sort = 'values'

	if sort == 'values':
		count_dict = dict(sorted(count_dict.items(), key=(lambda x: x[1]), reverse=True))
	else:
		count_dict = dict(sorted(count_dict.items()))

	# Modify dictionary before returning.
	if top:
		if type(top) == int:
			top_dict = dict()
			for item, _ in zip(count_dict, range(top)):
				top_dict[item] = count_dict[item]
			return top_dict
		else:
			raise TypeError(f'"top" must be an integer. Passed value is of type {type(top)}.')
	
	if min_val:
		if type(min_val) == int:
			min_val_dict = dict()
			for item in count_dict:
				if count_dict[item] >= min_val:
					min_val_dict[item] = count_dict[item]
			return min_val_dict

		else:
			raise TypeError(f'"min_val" must be an integer. Passed value is of type {type(min_val)}.')

	return count_dict

def filter_frame(df, term, col='subjects', strict=False):
	"""Return slice of DataFrame.

	Filter DataFrame based on presence of term in specified column (Default: "subjects").
	"""

	frame_check(df, col)

	# Filter out NA values.
	df = df.dropna(axis=0, subset=[col])

	if strict:
		# Matching exact content of cell.
		if not term in df[col].values:
			raise Exception(f'Passed term "{term}" not found in {col}.')

		filtered_frame = df[df[col] == term]

		return filtered_frame

	# Case-insensitive matching of cells containing term.
	filtered_frame = df[df[col].str.contains(term, case=False)]

	return filtered_frame


# USEFUL LISTS

# Member countries of NATO at the time of the fall of the Berlin Wall.
# NOTE: Based on inspection of data "United Kingdom" has been substituted by "Great Britain".
# For original list use 'nato_members_uk'.

nato_members = [
				'Belgium',
				'Canada',
				'Denmark',
				'France',
				'Iceland',
				'Italy',
				'Luxembourg',
				'Netherlands',
				'Norway',
				'Portugal',
				'Great Britain',
				'United States',
				'Greece',
				'Turkey',
				'West Germany',
				'Spain'
				]

nato_members_uk = nato_members.copy()
nato_members_uk[10] = 'United Kingdom'

# Equivalent list of nationalites/national adjectives of NATO member countries.
nato_adjectives = [
				'Belgium',
				'Canadian',
				'Danish',
				'French',
				'Icelandic',
				'Italian',
				'Luxembourg',
				'Dutch',
				'Norwegian',
				'Portuguese',
				'British',
				'American',
				'Greece',
				'West German',
				'Spanish'
				]

# List of KGB leaders 1954-1991.
# Source: https://en.wikipedia.org/wiki/KGB#List_of_chairmen
kgb_leaders = [
				'Serov',		# 1954–1958 
				'Shelepin',		# 1958–1961
				'Ivshutin',		# act. 1961
				'Semichastny',	# 1961–1967
				'Andropov',		# 1967–1982 (Jan.–May)
				'Fedorchuk',	# 1982 (May–Dec.)
				'Chebrikov',	# 1982–1988
				'Kryuchkov',	# 1988–1991
				'Shebarshin',	# act. 1991
				'Bakatin'		# 1991 (Aug.–Nov.)
				]