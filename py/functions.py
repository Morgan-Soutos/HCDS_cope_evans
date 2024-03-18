import pandas as pd
import numpy as np
#Some functions that might be helpful in processing data and avoiding duplicate code

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

def apply_dict(data: pd.DataFrame, dict: dict, columns: list[str]) -> pd.DataFrame:
    '''
    Applies the given dictionary to all of the given columns of the dataframe.

    Parameters:
        data (pd.DataFrame): The data that the dictionary is being applied to
        dict (dict): The dictionary being applied
        columns (list[str]): A list of columns that the dictionary is applied to
    
    Returns:
        data (pd.Dataframe): The dataframe with the dictionary applied.
    '''
    for column in columns:
        data = data.replace({column: dict})
    return data

def extract_date(data: pd.DataFrame, date_name: str) -> pd.DataFrame:
    '''
    Extracts the Year, Month, and Day from a column in the format YYYY-MM-DD

    Parameters:
        data (pd.Dataframe): The original dataframe
        date_name (str): The name of the column for dates
    
    Returns:
        data (pd.Dataframe): The input dataframe with new columns for Year, Month, and Day
    '''

    
    data = data[~data[date_name].str.contains('~')] #some entries have an estimate for the year, drop these

    data['Year'] = data[date_name].apply(lambda x: x[0:4])
    data['Month'] = data[date_name].apply(lambda x: x[5:7])
    data['Day'] = data[date_name].apply(lambda x: x[8:10])
    for column in ['Year', 'Month', 'Day']:
        data[column] = data[column].replace('', 0)
        data[column] = data[column].astype(int)
    return data

def create_location_dict(data, strings):
    locations = data['Origin']._append(data['Destination']).unique()
    location_dict = {}
    for string in strings:
        for location in locations:
            if string in location:
                location_dict[location] = string
    return location_dict
