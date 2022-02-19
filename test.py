from lib.tickers import Tickers

t = Tickers()
data = t.get_tickers()
print(data['tickers'][0])