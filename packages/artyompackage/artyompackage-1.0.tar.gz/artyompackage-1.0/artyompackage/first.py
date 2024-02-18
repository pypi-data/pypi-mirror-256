import pandas as pd

def load_data(filepath, file_type='csv'):
    """Load data from a file into a pandas DataFrame."""
    if file_type == 'csv':
        return pd.read_csv(filepath)
    elif file_type == 'excel':
        return pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file type. Please use 'csv' or 'excel'.")

def clean_data(dataframe, strategy='mean', columns=None):
    """Clean data by imputing missing values."""
    if columns is None:
        columns = dataframe.columns
    for column in columns:
        if strategy == 'mean':
            dataframe[column].fillna(dataframe[column].mean(), inplace=True)
        elif strategy == 'median':
            dataframe[column].fillna(dataframe[column].median(), inplace=True)
        elif strategy == 'delete':
            dataframe.dropna(subset=[column], inplace=True)
    return dataframe

from sklearn.preprocessing import StandardScaler, MinMaxScaler

def transform_data(dataframe, columns=None, method='standardize'):
    """Transform data columns using standardization or normalization."""
    scaler = StandardScaler() if method == 'standardize' else MinMaxScaler()
    if columns is None:
        columns = dataframe.columns
    dataframe[columns] = scaler.fit_transform(dataframe[columns])
    return dataframe

def summary_statistics(dataframe):
    """Return summary statistics for each column in the dataframe."""
    return dataframe.describe()

import matplotlib.pyplot as plt

def plot_data(dataframe, x, y, kind='line'):
    """Plot data from a dataframe."""
    if kind == 'line':
        dataframe.plot(x=x, y=y, kind='line')
    elif kind == 'scatter':
        dataframe.plot(x=x, y=y, kind='scatter')
    plt.show()
