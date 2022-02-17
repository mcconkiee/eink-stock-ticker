
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

# symbols = ["VIX","AAPL","SPY"]
symbols = ["VIX"]
for symbol in symbols:
    if symbol == "VIX":
        symbol = f"^{symbol}"
    
    logging.info(f"fetching symbol data•••: {symbol}")
    # can get symbls like "MSFT" or "^VIX" (note the karat)
    quote = get_symbol(symbol=symbol)
    history = get_history(symbol=symbol)
    # remove the karat if we have one
    symbol = symbol.replace("^","")
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
    im = Image.new("1", (width,height), bg_clr)
    d = ImageDraw.Draw(im)
    w, h = d.textsize(symbol, font=font)
    # smaller value == more left 
    x = w * .75
    # smaller value == more down
    y = h * 1.5
    
    logging.info("∞∞∞∞∞∞∞∞∞∞∞∞∞Quote X Y Position∞∞∞∞∞∞∞∞∞∞∞∞∞")
    logging.info(f"\r\ntextsize w = {w}\r\nh = {h}")
    logging.info(f"\r\nx = {x} \r\ny = {y}")
    
    d.text((x,y), symbol, fill=tx_clr, anchor="ms", font=font)
    d.text((x + padding, y+(sm + padding)), price, fill=tx_clr, anchor="ms", font=font_sm)
    d.text((x + padding, y+((sm + padding) * 2)), prcnt_w_symbol, fill=tx_clr, anchor="ms", font=font_sm)
    
    logging.info("creating chart image")
    # create chart
    chart_img = quickchart(width=int(width/5),height=int(height/2),dataset=history["Open"],background_clr=f"rgb({bg_clr},{bg_clr},{bg_clr})",line_clr=f"rgb({tx_clr},{tx_clr},{tx_clr})")    
    # get chart image
    chart = Image.open('imgs/chart.png') #.convert("RGBA")    
    back_im = im.copy()
    back_im.paste(chart,(round(width/1.75), 0),mask=chart)
    back_im.save('imgs/quote.png', quality=95)
    back_im.save(f"imgs/{symbol}.png", quality=95)

    logging.info("Display quote {symbol}")
    epd.display(epd.getbuffer(back_im))
    
    # # -----------_EXAMPLE_---------------------------------
    # logging.info("sleep 2 ")
    # time.sleep(2)
    # font24 = ImageFont.truetype(fnt, 24)
    # font18 = ImageFont.truetype(fnt, 18)
    # font35 = ImageFont.truetype(fnt, 35)
    # # Drawing on the Horizontal image
    # logging.info("1.Drawing on the Horizontal image...")
    # Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(Himage)
    # draw.text((10, 0), 'hello world', font = font24, fill = 0)
    # draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
    # draw.line((20, 50, 70, 100), fill = 0)
    # draw.line((70, 50, 20, 100), fill = 0)
    # draw.rectangle((20, 50, 70, 100), outline = 0)
    # draw.line((165, 50, 165, 100), fill = 0)
    # draw.line((140, 75, 190, 75), fill = 0)
    # draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # draw.rectangle((80, 50, 130, 100), fill = 0)
    # draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    # logging.info("dispaly demo ")
    # epd.Clear(0xFF)  
    # epd.display(epd.getbuffer(Himage))
    # # -----------_EXAMPLE_---------------------------------
