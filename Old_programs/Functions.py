import pandas as pd
import pandas_market_calendars as mcal
from datetime import datetime
import numpy as np
import random
import time
import csv

from alpaca.data import StockHistoricalDataClient, TimeFrame
from alpaca.data.requests import StockBarsRequest

# Functions

def connect():
    '''connects to Alpaca API returns data_client'''
    path = "../API_Keys/Alpaca_Keys.csv"
    with open(path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        API_KEY = next(csv_reader)[0]
        ALPACA_API_SECRET_KEY = next(csv_reader)[0]
        #TWELVE_DATA_KEY = next(csv_reader)[0]
    data_client = StockHistoricalDataClient(API_KEY, ALPACA_API_SECRET_KEY)
    return data_client

def trading_days(end_d, days_back):
    "Used in Create function; Formats the days"
    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(start_date=end_d - pd.Timedelta(days=days_back), end_date=end_d)
    td = schedule.index[0 : days_back] 
    return td

def call(start_date, stock, trading_days, percent_change, data_client):
    '''A subcall used for Create Data'''
    request_params = StockBarsRequest(
        symbol_or_symbols=[stock],            
        timeframe=TimeFrame.Day,
        start=start_date
    )

    # Fetch the bars data
    bars_data = data_client.get_stock_bars(request_params)
    bars_df = bars_data.df
    
    # Reset the index to separate the columns
    bars_df = bars_df.reset_index()

    # Convert the timezone of the timestamp column
    bars_df['timestamp'] = bars_df['timestamp'].dt.tz_convert('America/New_York')

    # Set the index back to symbol and timestamp if needed
    bars_df = bars_df.set_index(['symbol', 'timestamp'])

    #percent_change = [[0, 0] for i in range(len(trading_days))]
    for i in range(len(trading_days)):
        specific_date = pd.to_datetime(trading_days[i]).tz_localize('America/New_York')
        #print(specific_date)
        open_price = bars_df.loc[(stock, specific_date), 'open']
        close_price = bars_df.loc[(stock, specific_date), 'close']
        #percent_change[i][0] = f"{specific_date.date()} "
        #percent_change[i][1] = ((close_price/open_price)-1)*100
        percent_change.insert(0, [f"{specific_date.date()} ", ((close_price/open_price)-1)*100])
    return percent_change

def store_data(stock, percent_change):
    '''Stores Array of stocks within a CSV'''
    file_path = "Stocks/"+str(stock)+".csv"
    with open(file_path, mode='w', newline='') as file:   # w for a overwrite? 
        writer = csv.writer(file)
        writer.writerows(percent_change)
        
def add_ending(stock):
    '''Used to format ending of csv writing so while loop breaks at --,--'''
    file_path = "Stocks/"+str(stock)+".csv"
    with open(file_path, mode='a', newline='') as file:   # w for a overwrite? 
        writer = csv.writer(file)
        var = "end"
        writer.writerow(["--","--"])
              
def create_data(stock, days_back, data_client):
    '''Gets CSV data for the stock specficed and outputs in CSV file'''
    #break up days back into unders 150s calls
    today = pd.Timestamp.today(tz='America/New_York').normalize()
    percent_change = []
    
    count = days_back
    
    while(True):
        if count >= 200:
            td= trading_days(today - pd.Timedelta(days=count-200), 200) # start and end dates
            start_date = today - pd.Timedelta(days=count)
            call(start_date, stock, td, percent_change, data_client)
            count -= 200
            #print(f"1' delay at {count}")
           # time.sleep(60)
        else: 
            td= trading_days(today, count)
            start_date = today - pd.Timedelta(days=count)
            call(start_date, stock, td, percent_change, data_client)
            break
    store_data(stock, percent_change)
    add_ending(stock)

def all_stocks_1050(data_client):
    '''For all stocks in list it will write back 1050 days and convert into new csv for them'''
    path = "../Stocks-List.csv"
    with open(path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        Stock = next(csv_reader)[0]
        while Stock != "--":
            create_data(Stock, 1050, data_client)   # 250 workes   # 500 seems to work # a;sp 1050
            print(Stock)
            Stock = next(csv_reader)[0]
            print(Stock)
                     
def get_array(stock):
    '''Returns an array of the data from csv of stock'''
    path_stock = f"Stocks/{stock}.csv"
    stock_array = []

    with open(path_stock, mode='r', newline='') as stock:
        stock_reader = csv.reader(stock)
        while(True):
            stock_reader = next(csv.reader(stock))[1]
            if str(stock_reader) == "--":
                break
            stock_array.append(round(float(stock_reader) , 2))
    return stock_array  


def sum(array, start, end):
    '''return the total sum of an array'''
    sum = 0
    for i in range(end-start):
        sum += array[start+i]
    return sum
