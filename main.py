import logging
logging.basicConfig(level="DEBUG")
from lib.ticker_details import TickerDetails
# t = TickerDetails.from_symbol("SPY")
# logging.info(f"details = {t.current_symbol_data}")
# t.refresh()
from lib.tick import Tick

# standard loop for device 
# t = Tick().tick()

# Manual to not print to screen and save symbol data locally: eg: when debugging
t = Tick(symbols=["SPY"]).tick()
