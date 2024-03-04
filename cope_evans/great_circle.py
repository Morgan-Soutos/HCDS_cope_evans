'''Data processing for maps'''
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import pandas as pd

geo = pd.read_csv('csv/location and islandora - Finalized Geocoding.csv')
letters = pd.read_csv('csv/location and islandora - Data Sample (Box 3).csv')

data = pd.DataFrame(columns = ['Title', 'Description', 'Date Created', 'Origin', 'Destination', 'Author', 'start', 'end'])
data['Title'] = letters['Title']
data['Description'] = letters['Description']
data['Date Created'] = letters['Date Created']
data['Origin'] = letters['Origin']
data['Destination'] = letters['Destination']
data['Author'] = letters['Author']

data['start'] = data['Origin']
data['end'] = data['Destination']

def create_dict(dataframe: pd.DataFrame, columns: list[str], key: str) -> dict:
    '''
    Create a dictionary from a dataframe.

    Parameters:
        dataframe (pd.DataFrame): The dataframe being used to create a dictionary.
        columns (list[str]): The columns used to define the keys of the dictionary
        key (str): The column of the dataframe to be used as the outermost keys for the dictionary

    Returns:
        dict (dict): A dictionary with sub-dictionaries, with the general format of {key: {columns[1]: value, columns[2]: value, etc}}
    '''
    dict = pd.DataFrame(columns = columns)
    for column in columns:
        dict[column] = dataframe[column]
    dict = dict.drop_duplicates(key)
    dict.set_index(key, drop = True, inplace = True)
    dict = dict.to_dict(orient = 'index')
    return dict

def process(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    '''
    Process a dataframe by dropping NaNs and square brackets. 

    Parameters:
        data (pd.DataFrame): The dataframe being processed.
        columns (list[str]): A list of strings denoting the columns being changed.

    Returns:
        data (pd.DataFrame): The dataframe with only the rows for which the specified columns have no NaNs, with square brackets removed.
    '''
    for column in columns:
        data = data.dropna(subset = column)
    data = data.replace({'\[': '', '\]': ''}, regex = True)
    return data

def filter_dict(dict: dict):
    for key in list(dict.keys()):
        if key not in list:
            dict.pop()
    return dict

def apply_dict(data: pd.DataFrame, dict: dict, old_labels: list, new_labels: list):
    for label in old_labels:
        data = data.replace({label: dict})
        
        for l in new_labels:
            data[l] = data[label].apply(lambda x: x.get(l))


data = process(data, ['Origin', 'Destination'])
geo_dict = create_dict(geo, ['NACO', 'lat', 'long'], 'NACO')

""" for key in list(geo_dict.keys()):
    if key not in pd.concat([data['Origin'], data['Destination']]).unique():
        geo_dict.pop(key) """

data = data.replace({'start': geo_dict})
data = data.replace({'end': geo_dict})

data['start_lat'] = data['start'].apply(lambda x: x.get('lat'))
data['start_long'] = data['start'].apply(lambda x: x.get('long'))
data['end_lat'] = data['end'].apply(lambda x: x.get('lat'))
data['end_long'] = data['end'].apply(lambda x: x.get('long'))

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    locationmode = 'USA-states',
    lon = data['start_long'],
    lat = data['start_lat'],
    hoverinfo = 'text',
    text = data['Origin'],
    mode = 'markers',
    marker = dict(
        size = 2,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

for i in range(len(data)):
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'ISO-3',
            lon = [data['start_long'].iloc[i], data['end_long'].iloc[i]],
            lat = [data['start_lat'].iloc[i], data['end_lat'].iloc[i]],
            mode = 'lines',
            line = dict(width = 1,color = 'red'),
            text = [data['Author'].iloc[i]],
        )
    )

fig.update_layout(
    title_text = '',
    showlegend = False,
    geo = dict(
        scope = 'world',
        projection_type = 'azimuthal equal area',
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
)

fig.show()