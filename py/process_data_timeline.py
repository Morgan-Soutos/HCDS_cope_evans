import pandas as pd
from functions import *

letters = pd.read_csv('csv/location and islandora - Data Sample (Box 3).csv')

data = letters[['Title', 'Description', 'Date Created', 'Origin', 'Author', 'Recipient']]
data = process(data, ['Date Created'])

data = extract_date(data, 'Date Created')
data = data[data['Year'] >= 1820]
data = data[data['Year'] <= 1920]

data.to_csv('csv/processed_sample_data_timeline.csv')