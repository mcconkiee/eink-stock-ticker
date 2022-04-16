import yfinance as yf
import logging
from datetime import datetime, timedelta

# gets a symbol lik "^VIX" or "TSLA"
def get_symbol(symbol:str) -> yf.Ticker:
    vix = yf.Ticker(symbol)

    # show financials
    # vix.financials
    # vix.quarterly_financials    
    # # show major holders
    # vix.major_holders

    # # show institutional holders
    # vix.institutional_holders

    # # show balance sheet
    # vix.balance_sheet

    # # show news
    # vix.news
    return vix

""" 
in respect for history = tickr.history(period=period,interval=interval):

period: data period to download (Either Use period parameter or use start and end) Valid periods are: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
interval: data interval (intraday data cannot extend last 60 days) Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
start: If not using period - Download start date string (YYYY-MM-DD) or datetime.
end: If not using period - Download end date string (YYYY-MM-DD) or datetime.
prepost: Include Pre and Post market data in results? (Default is False)
auto_adjust: Adjust all OHLC automatically? (Default is True)
actions: Download stock dividends and stock splits events? (Default is True)
"""
def get_history(symbol:str,interval:str = "1d",period:str="3mo"):
    x=datetime.now()
    date_N_days_ago = datetime.now() - timedelta(days=1)
    fmt_start = date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d")
    fmt_end = x.strftime("%Y"+"-"+"%m"+"-"+"%d")    
    # data_df = yf.download(symbol,start=date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d"), interval=interval,period=period, end=x.strftime("%Y"+"-"+"%m"+"-"+"%d"))
    # return pandas dataframe
    # https://thepythonyouneed.com/how-to-get-the-length-and-width-of-a-pandas-dataframe-using-python/ 

    # return panda dataframe- eg history["Close"] gives all ticker values for all close sets
    #                            Open        High         Low       Close  Volume  Dividends  Stock Splits
    # Datetime                                                                                                  
    # 2022-01-28 09:30:00-05:00  295.620392  297.209991  295.149994  296.000000  863893          0             0
    # 2022-01-28 09:35:00-05:00  296.010010  296.040009  293.750000  294.920013  435657          0             0
    # 2022-01-28 09:40:00-05:00  295.000000  295.599915  294.019989  294.283997  323249          0             0
    try:        
        tickr = yf.Ticker(symbol)  
        history = tickr.history(period=period,interval=interval)        
        # history = tickr.history(start=fmt_start,end=fmt_end,interval=interval)        
        return history
    except Exception as error:
        logging.error(f"error collecting history for {symbol}")
        logging.error(error)
        raise error
