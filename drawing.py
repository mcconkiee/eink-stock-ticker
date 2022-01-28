
import json
from turtle import width
from lib.iex import fetch_quote
from lib.symbol import get_history, get_symbol
from lib.chart import quickchart
from lib.rapid_chart import get_chart
from PIL import Image, ImageDraw, ImageFont
fnt = "fonts/Arial Black.ttf"
tx_clr = "white"
bg_clr = "black"
lg = 100
sm = 30
padding = 10
width = 500
height = 200

symbols = ["VIX","AAPL","SPY"]
for symbol in symbols:
    if symbol == "VIX":
        symbol = f"^{symbol}"
    print(f"fetching symbol data•••: {symbol}")
    # can get symbls like "MSFT" or "^VIX" (note the karat)
    vix = get_symbol(symbol=symbol)
    history = get_history(symbol=symbol)
    # remove the karat if we have one
    symbol = symbol.replace("^","")
    print(f"SYMBOL: {json.dumps(vix.info)}")
    cur_price = float(vix.info.get('regularMarketPrice'))
    lst_price = float(vix.info.get('previousClose'))

    is_up = cur_price > lst_price
    price_diff = float(cur_price - lst_price) if is_up else float(lst_price - cur_price)
    price_diff = round(price_diff,2)

    delta = price_diff / cur_price
    prcnt = round(delta * 100,2)
    plus_minus = "-" if not is_up else "+"
    prcnt_w_symbol = f"{plus_minus}{price_diff} {plus_minus}{prcnt}%"
    # price = f"${cur_price} (${lst_price})"
    price = f"${cur_price}"

    font = ImageFont.truetype(fnt, lg if len(symbol)<=3 else int(lg * .75))
    font_sm = ImageFont.truetype(fnt, sm)
    # "RGB" vs "L" (grayscale)
    im = Image.new("RGB", (width,height), bg_clr)
    d = ImageDraw.Draw(im)
    w, h = d.textsize(symbol, font=font)
    # smaller == more left
    x = w * .65
    y = h * 1.05 - 15
    
    d.text((x,y), symbol, fill=tx_clr, anchor="ms", font=font)
    d.text((x + padding, y+(sm + padding)), price, fill=tx_clr, anchor="ms", font=font_sm)
    d.text((x + padding, y+((sm + padding) * 2)), prcnt_w_symbol, fill=tx_clr, anchor="ms", font=font_sm)

    # create chart
    chart_img = quickchart(width=int(width/5),height=int(height/2),dataset=history["Open"])
    # get chart image
    chart = Image.open('imgs/chart.png').convert("L")
    rapid_chart = get_chart(symbol="VIX")
    print(f"rapid chart = {rapid_chart}")
    back_im = im.copy()
    back_im.paste(chart,(round(width/1.75), 0))
    back_im.save('imgs/quote.png', quality=95)
    back_im.save(f"imgs/{symbol}.png", quality=95)



