
# import sys
# sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

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


from lib.tickers import Tickers
from time import time, sleep
from lib.iex import fetch_quote
from lib.symbol import get_history, get_symbol
from lib.chart import quickchart
from lib.rapid_chart import get_chart

HAS_EPD = False
if os.path.exists('/sys/'): 
    HAS_EPD = True
    from gpiozero import Button
    from lib.epd2in7 import EPD   

# configs
FWD = 5
BCKWRD = 6
RESET = 19
VIX = 13
chart_clr = 0xaa #https://www.color-hex.com
tx_clr = 0 # text color
bg_clr = 255 # white background

fnt = os.path.join(fontdir, 'Arial Black.ttf')
class Tick:
    epd = None
    btn1 = None
    btn2 = None
    btn3 = None
    btn4 = None
    logging.basicConfig(level=logging.INFO)
    symbols: list[str] = []
    
    # these are flipped on purpose
    rotate_img = False
    screen_width = 498
    screen_height = 300
    lg_font_size = 15 #large font
    sm_font_size = 10 #small font
    padding = 0

    counter  = 0 # increment/decrement on each cycle
    idx = 0 # keeps reference in our  tiker index
    increment = 1 # direction + || - 
    def __init__(self) -> None:    
        if HAS_EPD: 
            # setup epd
            _epd = EPD() # get the display
            self.rotate_img = True
            self.screen_width = _epd.height
            self.screen_height = _epd.width
            _epd.Init_4Gray()           # initialize the display
            logging.info("Clear display")    # prints to console, not the display, for debugging
            _epd.Clear(0xFF)   
            self.epd = _epd
            self.btn1.when_pressed = self.handleBtnPress
            self.btn2.when_pressed = self.handleBtnPress
            self.btn3.when_pressed = self.handleBtnPress
            self.btn4.when_pressed = self.handleBtnPress
    
        self.lg_font_size = int(self.screen_height/2) #large font
        self.sm_font_size = int(self.screen_height/8) #small font


    def update_msgs(self,msg:str,submsg:str = None,subsubmsg:str=None,display:bool=False,x:float=None,y:float=None):
        font = ImageFont.truetype(fnt, self.lg_font_size if len(msg)<=3 else int(self.lg_font_size * .75))
        font_sm = ImageFont.truetype(fnt, self.sm_font_size)    
        im = Image.new("L", (self.screen_width, self.screen_height), bg_clr)
        d = ImageDraw.Draw(im)
        w, h = d.textsize(msg, font=font)
        
        if x == None:
            x = self.screen_width/2  # 0 = left, width = right
        if y == None:
            y = self.screen_height - 30 #0 = top, height = bottom
        

        d.text((x,y), msg, fill=tx_clr, anchor="ms", font=font)
        if submsg:
            d.text((x + self.padding, y+(self.sm_font_size + self.padding)), submsg, fill=tx_clr, anchor="ms", font=font_sm)
        if subsubmsg:
            d.text((x + self.padding, y+((self.sm_font_size + self.padding) * 2)), subsubmsg, fill=tx_clr, anchor="ms", font=font_sm)
        if self.epd and display:
            self.epd.Clear(0xFF)  
            self.epd.display_4Gray(self.epd.getbuffer(im))
        return im


    def display_symbol(self,symbol:str):
        if symbol == "VIX":
            symbol = f"^{symbol}"
        orig_symbol = symbol.replace("^","")
        # update_msgs(msg=orig_symbol,submsg=f"...updating",display=True)    
        # can get symbls like "MSFT" or "^VIX" (note the karat)
        quote = get_symbol(symbol=symbol)    
        history = get_history(symbol=symbol)
        
        # remove the karat if we have one (eg ^VIX)
        symbol = orig_symbol
        # print(f"SYMBOL: {json.dumps(quote.info)}")
        cur_price = float(quote.info.get('regularMarketPrice'))
        lst_price = float(quote.info.get('previousClose'))

        is_up = cur_price > lst_price
        price_diff = float(cur_price - lst_price) if is_up else float(lst_price - cur_price)
        price_diff = round(price_diff,2)

        delta = price_diff / cur_price
        prcnt = round(delta * 100,2)
        plus_minus = "-" if not is_up else "+"
        prcnt_w_symbol = f"{plus_minus}{price_diff} {plus_minus}{prcnt}%"
        # price = f"${cur_price} (${lst_price})"
        price = f"${cur_price}"
        logging.info(f"{symbol} @  ${price} {prcnt_w_symbol}")

        # DRAW
        font = ImageFont.truetype(fnt, self.lg_font_size if len(symbol)<=3 else int(self.lg_font_size * .75))
        font_sm = ImageFont.truetype(fnt, self.sm_font_size)    

        # get prices to understand where is the chart line
        first_price = history["Open"][0]
        last_price = history["Open"][-1]
        length = history["Open"].shape[0]
        mid_price_idx = round(length/2)
        mid_price = history["Open"][mid_price_idx]
        # yvalue = (30 if mid_price < first_price  else height - 40)
        im = self.update_msgs(msg=symbol,submsg=price,subsubmsg=prcnt_w_symbol,y=100)
        
        # create chart
        
        chart_img = quickchart(
            width=int(self.screen_width/2),
            height=int(self.screen_height/2),
            dataset=history["Open"],
            background_clr=f"rgb({bg_clr},{bg_clr},{bg_clr})",
            line_clr=f"rgb({chart_clr},{chart_clr},{chart_clr})",
            saved_image_path=os.path.join(imgsdir,"chart.png"))    
        # get chart image
        # flip this image since we want the powersource on the bottom

        chart = Image.open(os.path.join(imgsdir,"chart.png")) #.convert("RGBA")    
        back_im = im.copy()        
        if self.rotate_img:
            chart = chart.transpose(PIL.Image.ROTATE_180)
            back_im = back_im.transpose(PIL.Image.ROTATE_180)
        back_im.paste(chart,(1, 1),mask=chart)
        back_im.save(os.path.join(imgsdir,"quote.png"), quality=95)
        
        back_im.save(os.path.join(imgsdir,f"{symbol}.png"), quality=95)
        
        logging.info("Display quote {symbol}")
        if self.epd:
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(back_im))    

    def get_tickers(self):
        t = Tickers()
        data = t.get_tickers()
        return data['tickers']

    def refresh(self):
        size = len(self.symbols)
        sleep_time = 30
        symbol = self.symbols[self.idx]
        logging.info(f"{symbol}••")
        try:
            self.display_symbol(symbol=symbol)
        except Exception as error:
            logging.DEBUG(f"error on symbol {symbol}")
            self.update_msgs(symbol=symbol,submsg=error.message,subsubmsg="",display=True)
            sleep_time = 10
        self.counter = (self.counter + self.increment) 
        self.idx = self.counter % size 
        sleep(sleep_time - time() % sleep_time)

    def tick(self):
        self.symbols = self.get_tickers()
        size = len(self.symbols)
        if size > 0:
            while True:                
                logging.info("fetching ")
                self.refresh()

    

    # https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8
    # https://gist.github.com/RaneWallin/fd73ddbffdabea23358f722adb9f4075
    def handleBtnPress(self,btn):
        if HAS_EPD:
            pinNum = btn.pin.number            
            if pinNum == FWD:
                self.increment = 1
                self.idx = self.idx + 1
                self.refresh()
            if pinNum == BCKWRD:
                self.increment = -1
                self.idx = self.idx - 1
                self.refresh()
            if pinNum == RESET:
                self.symbols = self.get_tickers()
                self.increment = 1
                self.counter = 0
                self.idx = 0     
                self.refresh()  
            if pinNum == VIX:
                self.display_symbol(symbol="VIX")
            



