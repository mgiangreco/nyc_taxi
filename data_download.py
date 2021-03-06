# Downloads yellow and green taxi data from NYC TLC dataset, described here:
# http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml
# WARNING: Very slow (each yellow file ~2GB)
# Compressed to about 1/4 the size in gzip format

import os
import requests
import glob
import pandas as pd

# Years of data to download 
years = ['2016']

# Months of data to download
months = ['06']

# Green only available beginning from August 2013
types = ['yellow', 'green']
url_add = 'https://s3.amazonaws.com/nyc-tlc/trip+data/'

# Set to download directory
os.chdir('/Users/mgiangreco/Documents/taxi_analysis/data')

# Get list of already downloaded files
files = glob.glob('yellow*') + glob.glob('green*')

for x in types:
    for y in years:
        for z in months:
            url_tmp = url_add + x + '_tripdata_' + y + '-' + z + '.csv'
            file_tmp = x + '_' + z + '_' + y + '.gz'
            if (file_tmp not in files) and (requests.head(url_tmp).status_code != 404):
                # Determine number of columns (from data dictionaries)
                col_list = list(range(0, 20)) if 'green' in file_tmp else list(range(0, 19))
                tmp_data = pd.read_csv(url_tmp, sep=',', index_col=False, usecols=col_list, 
                                       skip_blank_lines=True, error_bad_lines=False)
                tmp_data.to_csv(file_tmp, compression='gzip')
                del tmp_data
            print(file_tmp)