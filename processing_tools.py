import pandas as pd
import re
from helpers import frame_check, generate_filename

def relative_frequencies(df, term, col='text', strict=False):
    """Return Series of relative frequencies.

    Calculate relative frequencies of term in relation to total word count across column.
    """

    frame_check(df, col)

    word_counts = df[col].str.split().str.len()

    if strict:
        # Case-sensitive
        term_counts = df[col].str.count(term)
    else:
        # Case-insensitive
        term_counts = df[col].str.count(term, re.IGNORECASE)

    return pd.Series(term_counts / word_counts, name=term).fillna(0)


def group_years(df, fill_years=True, export=False, export_path='.'):
    """Return DataFrame with texts grouped by year.

    Texts are grouped based on year. By default, intermittent years without texts are included
    for a continuous timeline suitable for linear plotting.

    If needed for external analysis, texts grouped by year can be exported as .txt-files.
    """
    col = 'text'
    frame_check(df, col)

    # Drop rows without text.
    df = df[~df[col].str.contains('PDF')].copy()

    # Convert dates to datetime-format
    df.loc[:, 'date'] = pd.to_datetime(df['date'])

    # Create empty DataFrame indexed by year.
    year_frame = pd.DataFrame(columns=['doc_count', col], index=df['date'].dt.year.unique())

    # Iterate over years and insert texts accordingly.
    for year in year_frame.index:

        texts = list(df[df['date'].dt.year == year][col])

        year_text = '\n'.join(texts)

        year_frame.loc[year] = {'doc_count': len(texts), col: year_text}

        if export:
            # Export grouped texts to new text file.
            text_file = generate_filename(f"{export_path}/texts_{year}", 'txt', try_original=True)
            with open(text_file, 'w') as f:
                f.write(year_text)

    if fill_years:
        # Add empty years to DataFrame.
        # NOTE: Empty years at beginning and end of range are not included.
        for year in range(year_frame.index.min(), year_frame.index.max()):
            if not year in year_frame.index:
                year_frame.loc[year] = {'doc_count': 0, col: ''}

        # Sort index for coherent timeline.
        year_frame = year_frame.sort_index()

    return year_frame

def get_edges(df, col, sep=';'):
    """Returns list of edges (tuples of pairs) and a dictionary of values.
    """

    frame_check(df, col)

    # Prepare DataFrame for processing.
    df = df.dropna(axis=0, subset=[col])

    # Get rows with multiple values.
    df = df[df[col].str.contains(sep)]

    split_frame = df[col].str.split(sep, expand=True)

    row_list = split_frame.values.tolist()

    # Collapse list of lists and find unique values.
    flat_list = list()

    [[flat_list.append(item) for item in row if item and item not in flat_list] for row in row_list]

    flat_list = sorted(flat_list)

    # Generate dictionary of values and IDs for cross referencing.
    values = dict()

    for num, item in enumerate(flat_list):
        values[item] = num

    # Generate list of edges.
    edge_list = list()

    for row in row_list:
        for first_index, _ in enumerate(row):
            for second_index, _ in enumerate(row[first_index + 1:]):
                first_item = row[first_index]
                second_item = row[first_index + second_index + 1]
                if first_item and second_item:
                    edge_list.append((values[first_item], values[second_item]))

    return edge_list, values
