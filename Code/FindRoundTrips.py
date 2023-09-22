import pandas as pd



def find_number_of_round_trips(origin,destination):
    # importing the data and reading the csv file, be sure to change the file path
    csv_file_path = '/data/Flights.csv'
    data = pd.read_csv(csv_file_path)
    # Excluding the cancelled flights from the data
    filtered_flights_df_origin = data.loc[(data['ORIGIN'] == origin) & (data['CANCELLED'] == 0.0) & (data['DESTINATION'] == destination)]
    filtered_flights_df_destination = data.loc[(data['ORIGIN'] == destination) & (data['CANCELLED'] == 0.0) & (data['DESTINATION'] == origin)]
    filtered_flights_df = pd.concat([filtered_flights_df_origin,filtered_flights_df_destination])
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
    round_trip_routes = round_trip_counts_df.sort_values(by='round_trips', ascending=False).to_csv('financials/'+origin+'-'+destination+'-Flights.csv',index=False)
    return float(round_trip_counts_df['round_trips'].values[0])


def find_specific_round_trip(origin, destination):

    # importing the data and reading the csv file, be sure to change the file path
    csv_file_path = '/data/Flights.csv'
    data = pd.read_csv(csv_file_path)
    # Excluding the cancelled flights from the data
    filtered_flights_df_origin = data.loc[(data['ORIGIN'] == origin) & (data['CANCELLED'] == 0.0) & (data['DESTINATION'] == destination)]
    print(filtered_flights_df_origin.head(1))
