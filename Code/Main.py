import pandas as pd
import os

from FindProfit import *
from FindMostProfitableRoutes import *
# importing the data and reading the csv file

def find_busiest_and_most_profitable_round_trips(top_number_of_round_trips):
    ## Change the file path below
    csv_file_path = '/data/Flights.csv'
    data = pd.read_csv(csv_file_path)
    # Excluding the cancelled flights from the data
    filtered_flights_df = data[data['CANCELLED'] == 0.0]

    # Group by the pair of ORIGIN + DESTINATION to see how many trips there are in each direction 
    round_trip_counts = filtered_flights_df.groupby(['ORIGIN','DESTINATION']).size()
    round_trip_counts_df = round_trip_counts.reset_index(name='count')

    # Also get a count for the reverse trip, going from the DESTINATION back to the ORIGIN
    round_trip_counts_df['reverse_count'] = round_trip_counts_df.apply(
        lambda row: round_trip_counts.get((row['DESTINATION'], row['ORIGIN']), 0),
        axis=1
    )

    # The minimum value between the 'count' and the 'reverse_count' is the number of round trips
    round_trip_counts_df['round_trips'] = round_trip_counts_df[['count', 'reverse_count']].min(axis=1)

    # Give us the top 10 round trip routes by looking at the top 20 flights, reason I chose 20 is to look at the flights to the destination AND back.
    # The numbers should match up for the flight and the reverse flight.
    round_trip_counts_df['ROUTE'] = round_trip_counts_df.apply(lambda row: '-'.join([row['ORIGIN'], row['DESTINATION']]), axis=1)
    round_trip_routes = round_trip_counts_df.sort_values(by='round_trips', ascending=False).to_csv('all_round_trips.csv',index=False)
    top_10_round_trip_routes = round_trip_counts_df.sort_values(by='round_trips', ascending=False).head(top_number_of_round_trips*2)
    top_10_round_trip_routes.to_csv('top_'+str(top_number_of_round_trips)+'_round_trips.csv', index=False)
    print(top_10_round_trip_routes)
    list_num = 1
    for index, row in top_10_round_trip_routes[::2].iterrows():
        print(str(list_num)+': Route: '+row['ORIGIN']+'-'+row['DESTINATION'])
        route = row['ORIGIN']+'-'+row['DESTINATION']
        filename=route+'-Profit.csv'
        if filename not in os.listdir('financials'):
            most_profitable_round_trips(row['ORIGIN'],row['DESTINATION'])
        else:
            print('csv already created for '+route)
        list_num+=1
    create_most_profitable_csv(top_number_of_round_trips)

# Enter the number of the busiest round trips to analyze - around 2941 is the max (Note: analzying all the round trips will take ~2 hours).
find_busiest_and_most_profitable_round_trips(10)