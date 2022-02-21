
# import sys
# sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

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
from turtle import width
from lib.iex import fetch_quote
from lib.symbol import get_history, get_symbol
from lib.chart import quickchart
from lib.rapid_chart import get_chart


epd = None
if os.path.exists('/sys/'): 
    from gpiozero import Button
    from lib.epd2in7 import EPD   
    # setup epd
    epd = EPD() # get the display
    epd.Init_4Gray()           # initialize the display
    logging.info("Clear display")    # prints to console, not the display, for debugging
    epd.Clear(0xFF)  
logging.basicConfig(level=logging.INFO)
# paths
fnt = os.path.join(fontdir, 'Arial Black.ttf')
# configs
chart_clr = 0xaa #https://www.color-hex.com
tx_clr = 0 # text color
bg_clr = 255 # white background

# these are flipped on purpose
width = epd.height if epd else 250
height = epd.width if epd else 100
lg = int(height/2) #large font
sm = int(height/8) #small font
padding = 0

counter  = 0 # increment/decrement on each cycle
idx = 0 # keeps reference in our  tiker index
increment = 1 # direction + || - 

def update_msgs(msg:str,submsg:str = None,subsubmsg:str=None,display:bool=False,x:float=None,y:float=None):
    font = ImageFont.truetype(fnt, lg if len(msg)<=3 else int(lg * .75))
    font_sm = ImageFont.truetype(fnt, sm)    
    im = Image.new("L", (width,height), bg_clr)
    d = ImageDraw.Draw(im)
    w, h = d.textsize(msg, font=font)
    
    if x == None:
        x = width/2  # 0 = left, width = right
    if y == None:
        y = height - 30 #0 = top, height = bottom
    

    d.text((x,y), msg, fill=tx_clr, anchor="ms", font=font)
    if submsg:
        d.text((x + padding, y+(sm + padding)), submsg, fill=tx_clr, anchor="ms", font=font_sm)
    if subsubmsg:
        d.text((x + padding, y+((sm + padding) * 2)), subsubmsg, fill=tx_clr, anchor="ms", font=font_sm)
    if epd and display:
        epd.Clear(0xFF)  
        epd.display_4Gray(epd.getbuffer(im))
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
    # yvalue = (30 if mid_price < first_price  else height - 40)
    im = update_msgs(msg=symbol,submsg=price,subsubmsg=prcnt_w_symbol,y=100)
    
    # create chart
    
    chart_img = quickchart(
        width=int(width/2),
        height=int(height/2),
        dataset=history["Open"],
        background_clr=f"rgb({bg_clr},{bg_clr},{bg_clr})",
        line_clr=f"rgb({chart_clr},{chart_clr},{chart_clr})",
        saved_image_path=os.path.join(imgsdir,"chart.png"))    
    # get chart image
    # flip this image since we want the powersource on the bottom

    chart = Image.open(os.path.join(imgsdir,"chart.png")) #.convert("RGBA")    
    back_im = im.copy()
    rotate = True
    if rotate:
        chart = chart.transpose(PIL.Image.ROTATE_180)
        back_im = back_im.transpose(PIL.Image.ROTATE_180)
    back_im.paste(chart,(1, 1),mask=chart)
    back_im.save(os.path.join(imgsdir,"quote.png"), quality=95)
    
    back_im.save(os.path.join(imgsdir,f"{symbol}.png"), quality=95)
    
    logging.info("Display quote {symbol}")
    if epd:
        epd.display_4Gray(epd.getbuffer_4Gray(back_im))    

def get_tickers():
    t = Tickers()
    data = t.get_tickers()
    return data['tickers']

symbols = get_tickers()

def refresh(symbols):
    symbol = symbols[idx]
    logging.info(f"{symbol}••")
    try:
        display_symbol(symbol=symbol)
    except Exception as error:
        logging.DEBUG(f"error on symbol {symbol}")
        update_msgs(symbol=symbol,submsg=error.message,subsubmsg="",display=True)
        sleep_time = 10
    counter = (counter + increment) 
    idx = counter % size 
    sleep(sleep_time - time() % sleep_time)

# handle button taps
if epd:
    FWD = 5
    BCKWRD = 6
    RESET = 19
    VIX = 13
    btn1 = Button(FWD) # tick forward
    btn2 = Button(BCKWRD) # tick backwards
    btn3 = Button(VIX) # show vix
    btn4 = Button(RESET) # reset counter

    # https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8
    # https://gist.github.com/RaneWallin/fd73ddbffdabea23358f722adb9f4075
    def handleBtnPress(btn):
        pinNum = btn.pin.number
        refresh = True
        if pinNum == FWD:
            increment = 1
            idx = idx + 1
        if pinNum == BCKWRD:
            increment = -1
            idx = idx - 1
        if pinNum == RESET:
            symbols = get_tickers()
            increment = 1
            counter = 0
            idx = 0       
        if pinNum == VIX:
            refresh = False
            display_symbol(symbol="VIX")
        if refresh:
            refresh(symbols)


    btn1.when_pressed = handleBtnPress
    btn2.when_pressed = handleBtnPress
    btn3.when_pressed = handleBtnPress
    btn4.when_pressed = handleBtnPress


size = len(symbols)
if size > 0:
    while True:
        sleep_time = 30
        logging.info("fetching ")
        refresh(symbols)