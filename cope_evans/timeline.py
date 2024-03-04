'''Data processing for maps'''
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

letters = pd.read_csv('csv/location and islandora - Data Sample (Box 3).csv')

data = pd.DataFrame(columns = ['Title', 'Author', 'Description', 'Date Created', 'year', 'month', 'day', 'label'])

data['Title'] = letters['Title']
data['Author'] = letters['Author']
data['Description'] = letters['Description']
data['Date Created'] = letters['Date Created']

def process(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    '''
    Process a dataframe by dropping NaNs for specified column(s). 

    Parameters:
        data (pd.DataFrame): The dataframe being processed.
        columns (list[str]): A list of strings denoting the columns being changed.

    Returns:
        data (pd.DataFrame): The dataframe with only the rows for which the specified columns have no NaNs, with square brackets removed.
    '''
    for column in columns:
        data = data.dropna(subset = column)
    return data

data = process(data, ['Date Created'])
data['year'] = data['Date Created'].apply(lambda x: x[0:4])
data['month'] = data['Date Created'].apply(lambda x: x[5:7])
data['day'] = data['Date Created'].apply(lambda x: x[8:10])

data = data[data['year'].isin(['']) == False]
data = data[data['month'].isin(['']) == False]
data = data[data['day'].isin(['']) == False]

data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)


fig = px.scatter(data, x = data['year'], y = (data['month'] + data['day'] /31), hover_name = data['Title'],
                hover_data = 'Author',
                labels = {
                     'year': 'Year',
                     'y': 'Month'
                 })

fig.show()