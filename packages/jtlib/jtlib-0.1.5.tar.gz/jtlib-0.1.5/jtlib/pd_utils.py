#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns


TEMP_DIR = os.path.join(os.path.expanduser('~'), '.jtlib', 'temp')
ENCODING = 'ISO-8859-1'


def read_data_to_df(filepath, sheet_name=0, remove_unnamed=False, header='infer', multiple_tables=False):
    """
    Helper function for reading data into a pandas DataFrame.

    Args:
        (str) filepath - path to file containing data to be read.
        (boolean) remove_unnamed - Set to True to ignore columns without a header. Defaults to False.
        (int, list of int) header - Row number to use as the column names. Default to 'infer' column headers.
        (boolean) multiple_tables - If there are multiple tables, a list will be returned. Defaults to False.
    
    Returns:
        df - pandas DataFrame containing data read from the file.
    """

    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, encoding=ENCODING, low_memory=False, header=header)
    elif filepath.endswith('.htm'):
        df = pd.read_html(filepath, header=0)
        # If df is a list and multiple_tables=False, find the DataFrame with the most rows.
        if isinstance(df, list) and not multiple_tables:
            df_index = 1
            max_rows = 0
            for i, d in enumerate(df):
                rows = len(d.index)
                if rows > max_rows:
                    df_index = i
                    max_rows = rows

            # Set df to the DataFrame at the index we found
            # previously.
            df = df[df_index]
    else:
        df = pd.read_excel(filepath, sheet_name=sheet_name, engine='openpyxl')
    if remove_unnamed:
        df = remove_heading(df)
    return df


def remove_heading(df):
    if True in df.columns.str.contains('^Unnamed'):
        count = 0
        while True:
            if df.iloc[count].isnull().sum() > 0:
                count = count + 1
            else:
                break
        df.columns = df.iloc[count]
        df = df[count + 1:]
        df.reset_index(drop=True, inplace=True)


def append_dfs(dfs):
    """
    Appends dataframes together.

    Args:
        (list(pandas.DataFrame)) dfs - list of Pandas DataFrames
    Returns:
        df - a single Pandas DataFrame appended together from
             given list of dataframes
    """
    df_r = pd.DataFrame()

    print('Appending dataframes. This may take a few moments.')

    df_r = pd.concat(dfs)

    df_r.reset_index(drop=True, inplace=True)

    return df_r


def df_diff(df1, df2, columns=[]):
    if not columns:
        columns = df2.columns.tolist()
    df1['exist'] = 'exist'
    df = pd.merge(df2, df1, on=columns, how='left')
    df = df[df['exist'].isnull()].drop('exist', axis=1)
    df1.drop(columns=['exist'], inplace=True)
    return df


def normalize_columns(df):
    df = df.loc[:, df.columns.notnull()]
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'),
              inplace=True)

    return df


def explode_str(df, col, sep):
    s = df[col]
    i = np.arange(len(s)).repeat(s.str.count(sep) + 1)
    return df.iloc[i].assign(**{col: sep.join(s).split(sep)})


def create_time_series(start_date, end_date, frequency='d'):
    df = pd.DataFrame()
    df['Date'] = pd.date_range(start_date, end_date, freq=frequency)
    return df


def add_time_series(df, start_date=pd.to_datetime('20180101'), end_date=pd.to_datetime('today'), interval='30min'):
    df_time = create_time_series(start_date, end_date, '30min')
    df_time['Time'] = df_time['Date'].dt.time
    df_time['Date'] = df_time['Date'].dt.date
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    df = pd.merge(df_time, df, how='left', on=['Date', 'Time'])
    return df


def anti_join(first: pd.DataFrame, second: pd.DataFrame, on, merge='both'):
    df = pd.merge(first, second, how='outer', on=on, indicator = True)
    if merge == 'both':
        return df[~(df['_merge'] == 'both')].drop('_merge', axis = 1)
    else:
        return df[df['_merge'] == merge].drop('_merge', axis = 1)
    

def min_max_scale(df):
    return (df - df.min()) / (df.max() - df.min())
    

# Better looking heatmap. Source: https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec
def heatmap(df):
    corr = pd.melt(df.corr().reset_index(), id_vars='index')
    corr.columns = ['x', 'y', 'value']

    x = corr['x']
    y = corr['y']
    size = corr['value'].abs()

    fig, ax = plt.subplots()

    # color = [1]*len(x)

    # Create and map a color palette
    n_colors = 256
    palette = sns.diverging_palette(20, 220, n=n_colors)
    color_min, color_max = [-1, 1]

    def value_to_color(val):
        val_position = float((val - color_min)) / (color_max - color_min)
        # val_position = min(max(val_position, -1), 1)
        ind = int(val_position * (n_colors - 1))
        return palette[ind]

    
    # Mapping from column names to integer coordinates
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]:p[0] for p in enumerate(x_labels)}
    y_to_num = {p[1]:p[0] for p in enumerate(y_labels)}


    size_scale = 500

    # Create plot grid
    plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1)
    ax = plt.subplot(plot_grid[:,:-1])

    # Heatmap will take up the leftmost 14 grid spaces
    ax.scatter(x=x.map(x_to_num), y=y.map(y_to_num), s=size * size_scale, c=corr['value'].apply(value_to_color), marker='s')

    # Show column labels on the axes
    ax.set_xticks([x_to_num[v] for v in x_labels])
    ax.set_xticklabels(x_labels, rotation=45, rotation_mode='anchor', ha='left')
    ax.set_yticks([y_to_num[v] for v in y_labels])
    ax.set_yticklabels(y_labels)

    # Set grid lines to be between the axis ticks
    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)
    
    # Adjust the lower limits of each axis to remove cropping effect
    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])

    # Put labels and ticks on top
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    # Color legend
    ax = plt.subplot(plot_grid[:,-1])

    col_x = [0]*len(palette)
    bar_y = np.linspace(color_min, color_max, n_colors)

    bar_height = bar_y[1] - bar_y[0]

    ax.barh(y=bar_y, width=[5]*len(palette), left=col_x, height=bar_height, color=palette, linewidth=0)

    ax.set_xlim(1, 2)
    ax.grid(False)
    ax.set_facecolor('white')
    ax.set_xticks([])
    ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 3))
    ax.yaxis.tick_right()


if __name__ == '__main__':
    pass