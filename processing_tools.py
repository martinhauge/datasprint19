import pandas as pd
import re
from helpers import frame_check

def relative_frequencies(df, term, col='text', strict=False):
	"""Return Series of relative frequencies.

	Calculates relative frequencies of term in relation to total word count across column.
	"""

	frame_check(df, col)

	word_counts = df[col].str.split().str.len()

	if strict:
		# Case-sensitive
		term_counts = df[col].str.count(term)
	else:
		# Case-insensitive
		term_counts = df[col].str.count(term, re.IGNORECASE)

	return pd.Series(term_counts / word_counts, name=term)

def group_years(df, fill_years=True):
	"""Return DataFrame with texts grouped by year.

	Texts are grouped based on year. By default, intermittent years without texts are included
	for a continuous timeline suitable for linear plotting.
	"""
	col = 'text'
	frame_check(df, col)

	# Drop rows without text
	df = df[~df[col].str.contains('PDF')].copy()

	# Convert dates to datetime-format
	df.loc[:, 'date'] = pd.to_datetime(df['date'])

	# Create empty DataFrame indexed by year
	year_frame = pd.DataFrame(columns=['doc_count', col], index=df['date'].dt.year.unique())

	# Iterate over years and insert texts accordingly
	for year in year_frame.index:

		texts = list(df[df['date'].dt.year == year][col])

		year_text = '\n'.join(texts)

		year_frame.loc[year] = {'doc_count': len(texts), col: year_text}

		# ?TODO: Export data to txt-files

	if fill_years:
		# Add empty years to DataFrame.
		# NOTE: Empty years at beginning and end of range are not included.
		for year in range(year_frame.index.min(), year_frame.index.max()):
			if not year in year_frame.index:
				year_frame.loc[year] = {'doc_count': 0, col: ''}

		# Sort index for coherent timeline
		year_frame = year_frame.sort_index()

	return year_frame