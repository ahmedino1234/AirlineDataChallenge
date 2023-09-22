import pandas as pd
import re
from FindRoundTrips import *
import numpy as np

# Load in all the data, be sure to change the file path
flights_df = pd.read_csv('/data/Flights.csv')
airport_codes_df = pd.read_csv('/data/Airport_Codes.csv')
tickets_df = pd.read_csv('/data/Tickets.csv')


# This function is used to go through the tickets.csv file, find all the tickets for a specified route ('ORIGIN'-'DESTINATION), and find the average ticket fare
# by summing the total ITIN_FARE and total PASSENGERS and then dividing the total fare by the total number of passengers
def check_average_ticket_price(origin,destination):
    # Filter rows where ROUNDTRIP is 1.0
    route = origin+'-'+destination
    # round_trip_tickets_df = tickets_df[tickets_df['ROUNDTRIP'] == 1.0]
    # Create a new column called 'ROUTE' that is a combination of ORIGIN and DESTNATION values, sorted, with a hyphen in between.
    # This will make it easier for analysis and treat for example 'DCA' to 'JFK' round trip, the same as 'JFK' to 'DCA'
    filtered_tickets_df_origin = tickets_df.loc[(tickets_df['ORIGIN'] == origin) & (tickets_df['ROUNDTRIP'] == 1.0) & (tickets_df['DESTINATION'] == destination)]
    filtered_tickets_df_destination = tickets_df.loc[(tickets_df['ORIGIN'] == destination) & (tickets_df['ROUNDTRIP'] == 1.0) & (tickets_df['DESTINATION'] == origin)]
    # If statements to make sure none of the dataframes are empty
    if not filtered_tickets_df_origin.empty and not filtered_tickets_df_destination.empty:
        filtered_tickets_df = pd.concat([filtered_tickets_df_origin,filtered_tickets_df_destination])
    elif filtered_tickets_df_origin.empty and not filtered_tickets_df_destination.empty:
        filtered_tickets_df = filtered_tickets_df_destination
    elif not filtered_tickets_df_origin.empty and filtered_tickets_df_destination.empty:
        filtered_tickets_df = filtered_tickets_df_origin
    elif filtered_tickets_df_origin.empty and filtered_tickets_df_destination.empty:
        return 0
    filtered_tickets_df['ROUTE'] = filtered_tickets_df.apply(lambda row: '-'.join(sorted([row['ORIGIN'], row['DESTINATION']])), axis=1)
    filtered_tickets_df = filtered_tickets_df[['ITIN_ID','ROUTE', 'PASSENGERS', 'ITIN_FARE']]
    # Created a new df to store the average_ticket_price for the specified route
    average_ticket_prices_columns = ['ROUTE', 'TOTAL_PASSENGERS', 'TOTAL_ITIN_FARE', 'AVERAGE_ITIN_FARE']
    average_ticket_prices = pd.DataFrame(columns=average_ticket_prices_columns)
    total_passengers = 0
    total_itin_fare = 0
    for index, row in filtered_tickets_df.iterrows():
        route = row['ROUTE']
        passengers = float(row['PASSENGERS'])
        if type(row['ITIN_FARE']) == str:
            itin_fare = float(re.sub(r'[^0-9.]', '',row['ITIN_FARE']))
        else:
            itin_fare = row['ITIN_FARE']
        if (np.isnan(itin_fare) or np.isnan(passengers)):
            print('---')
        else:
            total_passengers += int(passengers)
            total_itin_fare += int(itin_fare)

    avg_ticket_price = total_itin_fare/total_passengers
    if pd.isna(avg_ticket_price):
            print('could not find avg fare for: ',route)
            return 0
    else:
        return round(avg_ticket_price,2)


# Function to find the costs due to delays
def delay_cost_calculator(delay):
    if pd.isna(delay) or delay<=15:
        return 0
    else:
        return (delay-15)*75

# Function to find the cost due to operation
def operational_cost_calculator(type_of_airport):
    if type_of_airport == 'large_airport':
        return 10000
    elif type_of_airport =='medium_airport':
        return 5000
    else:
        return None

# Function to find the total costs
def cost_calculator(dep_delay,arr_delay,distance,type_dest):
    delay_cost = (delay_cost_calculator(dep_delay)+(delay_cost_calculator(arr_delay)))
    if isinstance(distance, (float, int)):
        fuel_maintenance_cost = float(abs(distance))*9.18
    else:
        return None
    if type_dest == 'medium_airport' or type_dest == 'large_airport':
        operational_cost = operational_cost_calculator(type_dest)
    else:
        return None
    return (delay_cost + fuel_maintenance_cost + operational_cost)


#Function to find the total revenue
def revenue_calculator(occupancy_rate,avg_ticket_price):
    if isinstance(avg_ticket_price, (float, int)) and isinstance(occupancy_rate, (float, int)):
        ticket_sales = occupancy_rate*200*avg_ticket_price
        baggage_fees = (occupancy_rate)*200*35
        return ticket_sales+baggage_fees
    else:
        return None

# Function to find the profit for each flight, and then summing it all up in the end
def most_profitable_round_trips(origin, destination):
    # We first find the number of round trips as we set this as the limit when going through the flights.csv dataset
    limit = int(find_number_of_round_trips(origin,destination))
    filtered_flights_origin_df = flights_df.loc[(flights_df['ORIGIN'] == origin) & (flights_df['CANCELLED'] == 0.0) & (flights_df['DESTINATION'] == destination)].head(limit)
    filtered_flights_destination_df = flights_df.loc[(flights_df['ORIGIN'] == destination) & (flights_df['CANCELLED'] == 0.0) & (flights_df['DESTINATION'] == origin)].head(limit)
    filtered_flights_df = pd.concat([filtered_flights_origin_df,filtered_flights_destination_df])
    filtered_airport_codes_df = airport_codes_df[['TYPE','IATA_CODE']]
    if not filtered_flights_df.empty:
        # We merged the Flights.csv data with the Airport_Codes.csv data to find the airport type on the destination!
        merged_flight_data = pd.merge(filtered_flights_df, filtered_airport_codes_df, left_on='DESTINATION', right_on='IATA_CODE', how='left', suffixes=('','_DEST'))
        merged_flight_data['ROUTE'] = merged_flight_data.apply(lambda row: '-'.join(sorted([row['ORIGIN'], row['DESTINATION']])), axis=1)
        merged_flight_data = merged_flight_data[['ROUTE','TYPE','DISTANCE','OCCUPANCY_RATE','DEP_DELAY','ARR_DELAY']]

        avg_ticket_price = check_average_ticket_price(origin,destination)
        if avg_ticket_price is None:
            avg_ticket_price = 0

        total_revenue_tracker = 0
        profit_list = []
        for index, row in merged_flight_data.head(limit*2).iterrows():
            route = row['ROUTE']
            type_dest = row['TYPE']
            print('-------')
            distance = row['DISTANCE']
            occupancy_rate = row['OCCUPANCY_RATE']

            dep_delay = float(row['DEP_DELAY'])
            arr_delay = float(row['ARR_DELAY'])
            total_revenue_tracker+=1
            print(total_revenue_tracker)
            cost = cost_calculator(dep_delay,arr_delay,distance,type_dest)
            revenue = revenue_calculator(occupancy_rate,avg_ticket_price)
            if len(profit_list) > 0 and cost is not None and revenue is not None and pd.notna(cost) and pd.notna(revenue):
                profit = round(revenue - cost)
                print("profit is: $",profit)
                profit_list[0]['COST'] += cost
                profit_list[0]['REVENUE'] += revenue
                profit_list[0]['PROFIT'] += profit
            elif cost is not None and revenue is not None and pd.notna(cost) and pd.notna(revenue):
                profit = round(revenue - cost)
                new_entry = {'ROUTE':route,'COST':cost,'REVENUE':revenue,'PROFIT':profit}
                print(new_entry)
                profit_list.append(new_entry)

        # Finally, we have the total profit for this route!
        merged_flight_costs_revenue = pd.DataFrame(profit_list, columns=['ROUTE', 'COST', 'REVENUE','PROFIT'])
        print(merged_flight_costs_revenue)
        merged_flight_costs_revenue.to_csv('financials/'+origin+'-'+destination+'-Profit.csv', index=False)

