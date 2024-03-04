import pandas as pd
from functions import *

geo = pd.read_csv('csv/location and islandora - Finalized Geocoding.csv')
letters = pd.read_csv('csv/location and islandora - Data Sample (Box 3).csv')

data = letters[['Origin', 'Destination']]
data = process(data, ['Origin', 'Destination'])

data.to_csv('csv/processed_sample_data_networks.csv')