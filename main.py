import logging
logging.basicConfig(level="DEBUG")
from lib.ticker_details import TickerDetails
# t = TickerDetails.from_symbol("SPY")
# logging.info(f"details = {t.current_symbol_data}")
# t.refresh()
from lib.tick import Tick
t = Tick()
t.tick()
