#!/usr/bin/python

from time import sleep
from tick import Tick
try:
    t = Tick()    
    while True:
        t.tick()
        sleep(30)
except KeyboardInterrupt as e:
    logging.info("Stopping...")