import yfinance as yf

# gets a symbol lik "^VIX" or "TSLA"
def get_symbol(symbol:str):
    vix = yf.Ticker(symbol)

    # show financials
    vix.financials
    vix.quarterly_financials

    # show major holders
    vix.major_holders

    # show institutional holders
    vix.institutional_holders

    # show balance sheet
    vix.balance_sheet

    # show news
    vix.news
    return vix
