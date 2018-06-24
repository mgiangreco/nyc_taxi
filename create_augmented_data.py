import os
import glob
import pandas as pd
import numpy as np

# Augments the raw data to use in analysis. Only run this once!

# Set location of top directory
top_dir = '/Users/mgiangreco/Documents/taxi_analysis/'

# Set to number of decimals to round coordinates to
# 3 decimals provides ~ 100m resolution
num_dec = 3

# get necessary data files
os.chdir(top_dir + '/data')
files = glob.glob('green*') + glob.glob('yellow*')
pd_locations = pd.read_pickle('pd_locs.pkl')

#create locations dict
locations_dict = pd_locations.set_index(['rounded_lon', 'rounded_lat'], drop=True).to_dict('index')


for x in files:
    print(x)
    filename = x.split('.', 1)[0] + '_augmented.csv'
    tmp = pd.read_csv(x)
    tmp_col_names = [x.strip(' ').lower() for x in tmp.columns.values.tolist()]
    tmp_col_names = [x.replace('amt', 'amount') for x in tmp_col_names]
    tmp_col_names = [x.replace('start_lon', 'pickup_longitude') for x in tmp_col_names]
    tmp_col_names = [x.replace('start_lat', 'pickup_latitude') for x in tmp_col_names]
    tmp_col_names = ['pickup_time' if 'pickup_datetime' in x else x for x in tmp_col_names]
    tmp_col_names = ['dropoff_time' if 'dropoff_datetime' in x else x for x in tmp_col_names]
    tmp.columns = tmp_col_names
    tmp['rounded_pickup_lon'] = tmp.pickup_longitude.round(num_dec)
    tmp['rounded_pickup_lat'] = tmp.pickup_latitude.round(num_dec)
    tmp['pickup_latlong'] = tuple(zip(tmp.rounded_pickup_lon, tmp.rounded_pickup_lat))
    tmp['rounded_dropoff_lon'] = tmp.dropoff_longitude.round(num_dec)
    tmp['rounded_dropoff_lat'] = tmp.dropoff_latitude.round(num_dec)
    tmp['dropoff_latlong'] = tuple(zip(tmp.rounded_dropoff_lon, tmp.rounded_dropoff_lat))
    tmp['trip_time_in_secs'] = (pd.to_datetime(tmp.dropoff_time, format='%Y-%m-%d %H:%M:%S') - 
                                pd.to_datetime(tmp.pickup_time, format='%Y-%m-%d %H:%M:%S')).dt.seconds
    tmp['type'] = 'green' if 'green' in x else 'yellow'
    # lookup pickup and dropoff latlong borough and nbhd in dict and store in new cols
    tmp['pickup'] = pd.DataFrame.from_dict(tmp['pickup_latlong'].map(locations_dict))
    pickup_df = tmp['pickup'].apply(pd.Series)
    tmp['pickup_borough'] = pickup_df['borough']
    tmp['pickup_nbhd'] = pickup_df['nbhd']
    tmp['dropoff'] = pd.DataFrame.from_dict(tmp['dropoff_latlong'].map(locations_dict))
    tmp['dropoff'].apply(pd.Series)
    dropoff_df = tmp['dropoff'].apply(pd.Series)
    tmp['dropoff_borough'] = dropoff_df['borough']
    tmp['dropoff_nbhd'] = dropoff_df['nbhd']
    tmp.drop(['rounded_pickup_lon', 'rounded_pickup_lat', 'rounded_dropoff_lon', 'rounded_dropoff_lat', 'pickup', 'dropoff'], 
      axis=1, inplace=True)
    # save to csv
    tmp.to_csv(filename, index=False)
    del tmp
    
#tmp[['pickup_borough', 'pickup_nbhd']] = tmp['pickup'].apply(lambda x : pd.Series([x[0], x[1]]))




    
