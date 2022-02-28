#!/usr/bin/python
import logging
from time import sleep
from tick import Tick
logging.basicConfig(level=logging.INFO)
try:
    t = Tick()    
    while True:
        t.tick()
        sleep(30)
except KeyboardInterrupt as e:
    logging.info("Stopping...")