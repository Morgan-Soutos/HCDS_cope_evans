import pandas as pd
from functions import *

geo = pd.read_csv('csv/location and islandora - Finalized Geocoding.csv')
letters = pd.read_csv('csv/location and islandora - Data Sample (Box 3).csv')

data = letters[['Title', 'Description', 'Date Created', 'Origin', 'Author', 'Recipient']]
data = process(data, ['Origin', 'Date Created'])
data['Start'] = data['Origin']

geo_dict = create_dict(geo, ['NACO', 'lat', 'long'], 'NACO')
data = data[data['Origin'].apply(lambda x: x in geo['NACO'].unique())]

data = apply_dict(data, geo_dict, ['Start'])

data['start_lat'] = data['Start'].apply(lambda x: x.get('lat'))
data['start_long'] = data['Start'].apply(lambda x: x.get('long'))

data = extract_date(data, 'Date Created')
data = data[data['Year'] >= 1820]
data = data[data['Year'] <= 1920]

month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

season_dict = {}
for i in range(12):
    if (i + 1 in [3, 4, 5]):
        season_dict[i + 1] = 'Spring'
    if (i + 1 in [6, 7, 8]):
        season_dict[i + 1] = 'Summer'
    if (i + 1 in [9, 10, 11]):
        season_dict[i + 1] = 'Fall'
    if (i + 1 in [12, 1, 2]):
        season_dict[i + 1] = 'Winter'

data['Month Name'] = data['Month']
data['Season'] = data['Month']

data = data.replace({'Month Name': month_dict})
data = data.replace({'Season': season_dict})

data['Color'] = data['Season']

color_dict = {'Spring': 'green', 'Summer': 'yellow', 'Fall': 'orange', 'Winter': 'lightskyblue'}

data = data.replace({'Color': color_dict})

data.to_csv('csv/processed_sample_data_map.csv')