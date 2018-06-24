# nyc_taxi
Analysis of NYC taxi trip data

This repository provides Python code to download and analyze New York City taxi trips from June 2016, forked from [here] (https://github.com/geekman1/nyc_taxi) and modified to include dropoff as well as pickup locations and modified to return an unaggregated CSV file instead of a summarized file. A detailed description of the data is available [here](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml), as well as the actual data in CSV format. The directory should be set up as follows:

- Top Directory (called 'taxi_analysis' in the code)
  - Top Directory\data
  - Top Directory\notebooks
  
Make sure to download the 'nyc_neighborhoods.json' file to the top folder. This contains the GeoJSON data for New York City neighborhoods (polygon boundaries). The Python scripts should be run in the following order (make sure to update the top directory location path in each):
  
1. data_download.py (Downloads the trip data and saves to compressed gzip format files in the data directory.)
2. find_nbhd_centroids_boundaries.py (Finds and saves the neighborhood centroids and borders from the NYC neighborhoods JSON file.)
3. find_pickup_dropoff_nbhds.py (Finds the neighborhood and borough of each pickup and dropoff location in the full dataset by reverse geocoding the longitude/latitude coordinate pairs using the GeoJSON NYC neighborhoods file.)
4. create_augmented_data.py (Creates dataset augmented with pickup and dropoff locations, as well as trip time in secs.)


