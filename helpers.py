import pandas as pd
import os

def frame_check(df, col, col_type=str):
    """Check DataFrame and column name passed by user."""

    if not type(df) == pd.core.frame.DataFrame:
        raise TypeError('Data must be passed as a DataFrame.')

    if not type(col) == str:
        raise TypeError('Column name must be passed as a string.')
    
    if not col in df.columns:
        raise KeyError('Column not found in DataFrame. Please check column name.')

def generate_filename(base_name, extension, digits=2, try_original=False):
    """Return file name as string.

    Generate unique file name by incrementing suffix based on
    content of present directory.
    """
    
    extension = extension.strip('.')

    if try_original:
        original_name = f'{base_name}.{extension}'
        if not os.path.isfile(original_name):
            return original_name

    # Build template from arguments
    template = f'{base_name}_{{:0{digits}}}.{extension}'
    suffix = 1

    # Initial file name
    file_name = template.format(suffix)

    # Increment suffix until unused file name is found
    while os.path.isfile(file_name):
        suffix += 1
        file_name = template.format(suffix)

    return file_name