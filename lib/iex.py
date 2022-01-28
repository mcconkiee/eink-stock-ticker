# NOTE - NOT using this currently, but EX was another option to collect data
import pyEX as p

from os import environ
TOKEN=environ.get('EX_TOKEN')
class IEQuote:
    def __init__(self, quote, chart):
        self.quote = quote
        self.chart = chart
def fetch_quote(symbol:str,range:str = "1m", last:int = 500):
    c = p.Client()
    quote = c.quote(symbol)
    chart = c.chart(symbol)
    return IEQuote(quote=quote,chart=chart)