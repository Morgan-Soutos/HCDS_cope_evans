import pandas as pd
from functions import *

geo = pd.read_csv('csv/location and islandora - Finalized Geocoding.csv')
letters = pd.read_csv('csv/location and islandora - 1820-1920.csv')

data = letters[['Origin', 'Destination']]
data = process(data, ['Origin', 'Destination'])

data_simplified = data.copy(True)

location_dict = create_location_dict(data_simplified, ['Philadelphia, Pa.', 'England', 'France', 'Switzerland', 'Italy', 'Ireland', 'Scotland', 'Minn.', 'N.Y.', 'N.J.', 'Susquehanna County', 'M.d.', 'Netherlands', 'W. Va.', 'Va.', 'N.H.', 'R.I.', 'R.I', 'Me.', 'Del.', 'La.', 'S.C', 'Ohio', 'Mass.', 'Mich.', 'Md.', 'Iraq', 'N.C.', 'Conn.', 'Ind.', 'Ga.', 'Fla.', 'Calif.', 'Iowa', 'Ky.'])



data_simplified = data_simplified.replace({'Origin': location_dict})
data_simplified = data_simplified.replace({'Destination': location_dict}) 
data_simplified = data_simplified.replace(to_replace='Philadelphia (Pa.)', value='Philadelphia') 
data_simplified = data_simplified.replace(to_replace='Philadelphia, Pa.', value='Philadelphia') 

location_dict2 = create_location_dict(data_simplified, ['Pa.'])
data_simplified = data_simplified.replace({'Origin': location_dict2})
data_simplified = data_simplified.replace({'Destination': location_dict2}) 
data_simplified = data_simplified.replace(to_replace='Pa.', value='Pennsylvania') 
data_simplified = data_simplified.replace(to_replace='N.Y.', value='New York (State)') 
data_simplified = data_simplified.replace(to_replace='N.J.', value='New Jersey') 
data_simplified = data_simplified.replace(to_replace='Mass.', value='Massachusetts') 
data_simplified = data_simplified.replace(to_replace='Conn.', value='Connecticut') 
data_simplified = data_simplified.replace(to_replace='N.H.', value='New Hampshire') 
data_simplified = data_simplified.replace(to_replace='Mich.', value='Michigan') 
data_simplified = data_simplified.replace(to_replace='N.C.', value='North Carolina') 
data_simplified = data_simplified.replace(to_replace='R.I.', value='Rhode Island') 
data_simplified = data_simplified.replace(to_replace='R.I', value='Rhode Island') 
data_simplified = data_simplified.replace(to_replace='Va.', value='Virginia') 
data_simplified = data_simplified.replace(to_replace='W. Va.', value='West Virginia') 
data_simplified = data_simplified.replace(to_replace='Calif.', value='California') 
data_simplified = data_simplified.replace(to_replace='Ga.', value='Georgia') 
data_simplified = data_simplified.replace(to_replace='Md.', value='Maryland') 
data_simplified = data_simplified.replace(to_replace='Me.', value='Maine') 
data_simplified = data_simplified.replace(to_replace='S.C.', value='South Carolina') 
data_simplified = data_simplified.replace(to_replace='S.C', value='South Carolina') 
data_simplified = data_simplified.replace(to_replace='Fla.', value='Florida') 
data_simplified = data_simplified.replace(to_replace='Ky.', value='Kentucky') 
data_simplified = data_simplified.replace(to_replace='Del.', value='Delaware') 
data_simplified = data_simplified.replace(to_replace='La.', value='Louisiana') 
data_simplified = data_simplified.replace(to_replace='Ind.', value='Indiana') 
data_simplified = data_simplified.replace(to_replace='Minn.', value='Minnesota') 

data.to_csv('csv/processed_data_networks.csv')
data_simplified.to_csv('csv/processed_data_networks_simplified.csv')