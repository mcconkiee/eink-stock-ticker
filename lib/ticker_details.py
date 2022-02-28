from mimetypes import init
import sys
import os
srcdir = os.path.dirname(os.path.realpath(__file__))
fontdir = os.path.join(srcdir,"fonts")
imgsdir = os.path.join(srcdir,"imgs")

import json
import logging
import PIL
from PIL import Image, ImageDraw, ImageFont

from gpiozero import Button
from lib.tickers import Tickers
from time import time, sleep
from lib.iex import fetch_quote
from lib.symbol import get_history, get_symbol
from lib.chart import quickchart
from lib.rapid_chart import get_chart
SLEEPTIME = 25
HAS_EPD = False
if os.path.exists('/sys/'):
    HAS_EPD = True
    from lib.epd2in7 import EPD   

chart_clr = 0xaa #https://www.color-hex.com
tx_clr = 0 # text color
bg_clr = 255 # white background

fnt = os.path.join(fontdir, 'Arial Black.ttf')
class TickerDetails:
    def __init__(self,symbol:str) -> None:
        self.symbol = symbol
    def draw(self):
        font = ImageFont.truetype(fnt, self.sm_font_size)
        im = Image.new("L", (self.screen_width, self.screen_height), bg_clr)
        d = ImageDraw.Draw(im)
        padding =  -20
        # data
        symbol = self.symbols[self.idx]
        quote = get_symbol(symbol=symbol)    
        orig_symbol = symbol.replace("^","")
        info = quote.info
        # copy
        high = f"high: {info.get('fiftyTwoWeekHigh')}"
        low = f"low: {info.get('fiftyTwoWeekLow')}"
        msg = f"{orig_symbol}"
        # size/dimensions
        w_msg, h_msg = d.textsize(msg, font=font)
        w_high, h_high = d.textsize(high, font=font)
        w_low, h_low = d.textsize(low, font=font)        
        # draw
        d.text((w_msg + padding,h_msg), msg, fill=tx_clr, anchor="ms", font=font)
        d.text((w_high + padding,h_msg + h_high), f"high: {high}", fill=tx_clr, anchor="ms", font=font)
        d.text((w_low + padding,h_msg + h_high + h_low), f"low: {low}", fill=tx_clr, anchor="ms", font=font)
        if self.epd :
            self.epd.Clear(0xFF)  
            if self.rotate_img:
                im = im.transpose(PIL.Image.ROTATE_180)
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(im))