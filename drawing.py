
# import sys
# sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

import sys
import os
srcdir = os.path.dirname(os.path.realpath(__file__))
fontdir = os.path.join(srcdir,"fonts")
imgsdir = os.path.join(srcdir,"imgs")


# import lib.epd2in7b
from lib.epd2in7 import EPD
import json
import logging
from time import time, sleep
from turtle import width
from lib.iex import fetch_quote
from lib.symbol import get_history, get_symbol
from lib.chart import quickchart
from lib.rapid_chart import get_chart
from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(level=logging.INFO)

fnt = os.path.join(fontdir, 'Arial Black.ttf')

tx_clr = 0
bg_clr = 255



epd = EPD() # get the display
epd.init()           # initialize the display
logging.info("Clear display")    # prints to console, not the display, for debugging
epd.Clear(0xFF)  

# these are flipped on purpose
width = epd.height
height = epd.width 
logging.info(f"§¶¶¶§§§§§§§§§§§§")
logging.info(f"\r\n{width} = width \r\n {height} =  height")
logging.info(f"§¶¶¶§§§§§§§§§§§§")
lg = int(height/8)
sm = int(height/13)
padding = 0


def update_msgs(msg:str,submsg:str = None,subsubmsg:str=None,display:bool=False,x:float=None,y:float=None):
    font = ImageFont.truetype(fnt, lg if len(msg)<=3 else int(lg * .75))
    font_sm = ImageFont.truetype(fnt, sm)    
    im = Image.new("1", (width,height), bg_clr)
    d = ImageDraw.Draw(im)
    w, h = d.textsize(msg, font=font)
    
    if x == None:
        x = width/2 - w/4 # 0 = left, width = right
    if y == None:
        y = height - 30 #0 = top, height = bottom
    

    d.text((x,y), msg, fill=tx_clr, anchor="ms", font=font)
    if submsg:
        d.text((x + padding, y+(sm + padding)), submsg, fill=tx_clr, anchor="ms", font=font_sm)
    if subsubmsg:
        d.text((x + padding, y+((sm + padding) * 2)), subsubmsg, fill=tx_clr, anchor="ms", font=font_sm)
    if display:
        epd.Clear(0xFF)  
        epd.display(epd.getbuffer(im))
    return im

def display_symbol(symbol:str):
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
    logging.info(f"••••••••••••••••SYMBOL DATA••••••••••••••••••••••")
    logging.info(f"{symbol} @  ${price} {prcnt_w_symbol}")

    # DRAW
    font = ImageFont.truetype(fnt, lg if len(symbol)<=3 else int(lg * .75))
    font_sm = ImageFont.truetype(fnt, sm)    

    # get prices to understand where is the chart line
    first_price = history["Open"][0]
    last_price = history["Open"][-1]
    length = history["Open"].shape[0]
    mid_price_idx = round(length/2)
    mid_price = history["Open"][mid_price_idx]
    yvalue = (height + (height - 50) if mid_price < first_price  else height - 50)
    im = update_msgs(msg=symbol,submsg=price,subsubmsg=prcnt_w_symbol,y=yvalue)
    
    logging.info("creating chart image")
    # create chart
    lt_gray = tx_clr - 40
    chart_img = quickchart(
        width=int(width/2),
        height=int(height/2),
        dataset=history["Open"],
        background_clr=f"rgb({bg_clr},{bg_clr},{bg_clr})",
        line_clr=f"rgb({lt_gray},{lt_gray},{lt_gray})",
        saved_image_path=os.path.join(imgsdir,"chart.png"))    
    # get chart image
    
    chart = Image.open(os.path.join(imgsdir,"chart.png")) #.convert("RGBA")    
    back_im = im.copy()
    back_im.paste(chart,(1, 1),mask=chart)
    back_im.save(os.path.join(imgsdir,"quote.png"), quality=95)
    
    back_im.save(os.path.join(imgsdir,f"{symbol}.png"), quality=95)

    logging.info("Display quote {symbol}")
    epd.display(epd.getbuffer(back_im))    

symbols = ["VIX","AAPL","SPY"]
counter  = 0
while True:
    logging.info("fetching ")
    symbol = symbols[counter]
    logging.info(f"{symbol}••")
    display_symbol(symbol=symbol)
    counter = (counter + 1) 
    idx = counter % len(symbols)
    sleep(60 - time() % 60)