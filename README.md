# Airline Data Challenge
Consulting for an airline company looking to enter the United States domestic market, we are tasked with finding 5 round trip routes for it to start serving. Considering revenue, cost, and overall profit, we must advise which round trip routes to recommend to this new airline based on the (mock) data provided.


## Problem Statement

You are consulting for an airline company looking to enter the United States domestic market
which has identified medium and large airports as their desired operating locations. The
company believes that it has a competitive advantage in maintaining punctuality, so it plans on
making this a big part of its brand image with a motto, “On time, for you.” To kick start
operations, the company has decided to start with 5 round trip routes. An example of a round
trip route is the combination of JFK to ORD and ORD to JFK. The opposite order of the
route, ORD to JFK and JFK to ORD, would be considered the same round trip.
You have been tasked with analyzing 1Q2019 data to identify:

1. The 10 busiest round trip routes in terms of number of round trip flights in the quarter.
Exclude canceled flights when performing the calculation.

2. The 10 most profitable round trip routes (without considering the upfront airplane cost) in
the quarter. Along with the profit, show total revenue, total cost, summary values of other
key components and total round trip flights in the quarter for the top 10 most profitable
routes. Exclude canceled flights from these calculations.

3. The 5 round trip routes that you recommend to invest in based on any factors that you
choose.

4. The number of round trip flights it will take to breakeven on the upfront airplane cost for
each of the 5 round trip routes that you recommend. Print key summary components for
these routes.

5. Key Performance Indicators (KPI’s) that you recommend tracking in the future to
measure the success of the round trip routes that you recommend.
You have been given a metadata document and three datasets that you should use to inform
your decision:
- Flights dataset: Contains data about available routes from origin to destination. For
occupancy, use the data provided in this dataset.
- Tickets dataset: Ticket prices data (randomly sampled data only as the original dataset
data is huge). Consider only round trips in your analysis.
- Airport Codes dataset: Identifies whether an airport is considered medium or large
sized. Consider only medium and large airports in your analysis.


### You can make the following assumptions:
● Each airplane is dedicated to one round trip route between the 2 airports

#### Costs:
○ Fuel, Oil, Maintenance, Crew - $8 per mile total
○ Depreciation, Insurance, Other - $1.18 per mile total
○ Airport operational costs for the right to use the airports and related services are
fixed at $5,000 for medium airports and $10,000 for large airports. There is one
charge for each airport where a flight lands. Thus, a round trip flight has a total of
two airport charges.
○ Delays that are 15 minutes or less are free, however each additional minute of
delay costs the airline $75 in added operational costs. This is charged separately
for both arrival and departure delays.
○ Each airplane will cost $90 million

#### Revenue:
○ Each plane can accommodate up to 200 passengers and each flight has an
associated occupancy rate provided in the Flights data set. Do not use the
Tickets data set to determine occupancy.
○ Baggage fee is $35 for each checked bag per flight. We expect 50% of
passengers to check an average of 1 bag per flight. The fee is charged
separately for each leg of a round trip flight, thus 50% of passengers will be
charged a total of $70 in baggage fees for a round trip flight.
○ Disregard seasonal effects on ticket prices (i.e. ticket prices are the same in April
as they are on Memorial Day or in December)

## Results

After analyzing the data, the 5 round trip routes that I recommend to invest in based on overall profit, maximum revenue,
and minimum cost are:
1. CLT-GSP (Charlotte, NC - Greer, SC)
2. CLT-GSO (Charlotte. NC - Greensboro, NC)
3. CHS-CLT (Charleston, SC - Charlotte, NC)
4. CLT-ILM (Charlotte, NC - Wilmington, NC)
5. ATL-CLT (Atlanta, GA - Charlotte, NC)

As we can see, all five of the most profitable routes start or end in Charlotte, North Carolina, and are
flights that are very short in duration, going to nearby states on the East Coast.

Exact metrics can be seen in the visuals under the visuals folder, and a more extensive write up can be provided upon request.


## Code

The script might be a lot to process at first glance. The main file, 'main.py', is where the script begins. Within that file, we have a function
"find_busiest_and_most_profitable_round_trips" with a single parameter; this parameter is an integer that represents of how many of the busiest round trips 
we want to analyze to determine total cost, revenue, and profit. For example, if we were to put the number 10, the script would create a csv and determine the most profitable round trip of the top 10 busiest
round trips in the dataset. 

Simply change the parameter, make sure the csv paths are pointing to the files on your local machine, and you are good to go!
