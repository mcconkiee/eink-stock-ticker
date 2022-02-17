
# import sys
# sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

# import lib.epd2in7b
from lib.epd2in7 import EPD
import json
import logging
import time
from turtle import width
from lib.iex import fetch_quote
from lib.symbol import get_history, get_symbol
from lib.chart import quickchart
from lib.rapid_chart import get_chart
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

fnt = "fonts/Arial Black.ttf"
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
lg = int(height/3)
sm = int(height/8)
padding = 0


def update_msgs(msg:str,submsg:str = None,subsubmsg:str=None,display:bool=False):
    font = ImageFont.truetype(fnt, lg if len(msg)<=3 else int(lg * .75))
    font_sm = ImageFont.truetype(fnt, sm)    
    im = Image.new("1", (width,height), bg_clr)
    d = ImageDraw.Draw(im)
    w, h = d.textsize(msg, font=font)
    # smaller value == more left 
    x = w * .75
    # smaller value == more down
    y = h * .75    
    
    logging.info("∞∞∞∞∞∞∞∞∞∞∞∞∞Quote X Y Position∞∞∞∞∞∞∞∞∞∞∞∞∞")
    logging.info(f"\r\ntextsize w = {w}\r\nh = {h}")
    logging.info(f"\r\nx = {x} \r\ny = {y}")

    d.text((x,y), msg, fill=tx_clr, anchor="ms", font=font)
    if submsg:
        d.text((x + padding, y+(sm + padding)), submsg, fill=tx_clr, anchor="ms", font=font_sm)
    if subsubmsg:
        d.text((x + padding, y+((sm + padding) * 2)), subsubmsg, fill=tx_clr, anchor="ms", font=font_sm)
    if display:
        epd.Clear(0xFF)  
        epd.display(epd.getbuffer(im))
    return im


# symbols = ["VIX","AAPL","SPY"]
symbols = ["VIX"]
for symbol in symbols:
    if symbol == "VIX":
        symbol = f"^{symbol}"
    orig_symbol = symbol.replace("^","")
    update_msgs(msg=orig_symbol,submsg="...updating",display=True)
    logging.info(f"fetching symbol data•••: {symbol}")
    # can get symbls like "MSFT" or "^VIX" (note the karat)
    quote = get_symbol(symbol=symbol)    
    history = get_history(symbol=symbol)
    logging.debug(f"QUOTE•••:\r\n {quote}\r\n{history}")

    # remove the karat if we have one
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

    im = update_msgs(symbol,price,prcnt_w_symbol)
    
    logging.info("creating chart image")
    # create chart
    chart_img = quickchart(width=int(width),height=int(height/2),dataset=history["Open"],background_clr=f"rgb({bg_clr},{bg_clr},{bg_clr})",line_clr=f"rgb({tx_clr},{tx_clr},{tx_clr})")    
    # get chart image
    chart = Image.open('imgs/chart.png') #.convert("RGBA")    
    back_im = im.copy()
    back_im.paste(chart,(5, 100),mask=chart)
    back_im.save('imgs/quote.png', quality=95)
    back_im.save(f"imgs/{symbol}.png", quality=95)

    logging.info("Display quote {symbol}")
    epd.display(epd.getbuffer(back_im))
    

