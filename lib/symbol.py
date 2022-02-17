import yfinance as yf
from datetime import datetime, timedelta

# gets a symbol lik "^VIX" or "TSLA"
def get_symbol(symbol:str):
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

def get_history(symbol:str,interval:str = "5m",period:str="1d"):
    x=datetime.now()
    date_N_days_ago = datetime.now() - timedelta(days=1)
    fmt_start = date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d")
    fmt_end = x.strftime("%Y"+"-"+"%m"+"-"+"%d")    
    # data_df = yf.download(symbol,start=date_N_days_ago.strftime("%Y"+"-"+"%m"+"-"+"%d"), interval=interval,period=period, end=x.strftime("%Y"+"-"+"%m"+"-"+"%d"))
    # return data_df

    # return panda dataframe- eg history["Close"] gives all ticker values for all close sets
    #                                     Open        High         Low       Close  Volume  Dividends  Stock Splits
    # Datetime                                                                                                  
    # 2022-01-28 09:30:00-05:00  295.620392  297.209991  295.149994  296.000000  863893          0             0
    # 2022-01-28 09:35:00-05:00  296.010010  296.040009  293.750000  294.920013  435657          0             0
    # 2022-01-28 09:40:00-05:00  295.000000  295.599915  294.019989  294.283997  323249          0             0
    tickr = yf.Ticker(symbol)  
    history = tickr.history(period=period,interval=interval)
    # history = tickr.history(start=fmt_start,end=fmt_end,interval=interval)        
    return history
