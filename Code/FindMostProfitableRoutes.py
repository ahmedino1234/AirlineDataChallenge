import os
import pandas as pd


# Function to create a combined csv of all the routes and showcase their COST, REVENUE, and PROFIT
def create_most_profitable_csv(num_input):
    profit_list = []
    most_profitable_columns = ['ROUTE', 'COST','REVENUE','PROFIT']
    most_profitable_df = pd.DataFrame(columns=most_profitable_columns)
    for filename in os.listdir('financials'):
        if '-Profit' in filename:
            f = os.path.join('financials', filename)
            if os.path.isfile(f):
                df = pd.read_csv(f)
                if not df.empty:
                    new_entry = {'ROUTE':df['ROUTE'].values[0],'COST':df['COST'].values[0],'REVENUE':df['REVENUE'].values[0],'PROFIT':df['PROFIT'].values[0]}
                    profit_list.append(new_entry)
    # Once that list is made, convert it to a dataframe and drop any duplicates to ensure data quality
    most_profitable_df = pd.DataFrame(profit_list, columns=['ROUTE', 'COST', 'REVENUE','PROFIT'])
    most_profitable_df = most_profitable_df.drop_duplicates(subset=['ROUTE'])
    most_profitable_df.sort_values(by=['PROFIT'],ascending=False).to_csv('Top_'+str(num_input)+'_Most_Profitable_Round_Trips.csv',index=False)
    print(most_profitable_df.sort_values(by=['PROFIT'],ascending=False))

