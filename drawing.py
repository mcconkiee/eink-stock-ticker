
import json
from lib.symbol import get_symbol
from PIL import Image, ImageDraw, ImageFont
fnt = "fonts/Arial Black.ttf"
tx_clr = "white"
bg_clr = "black"
lg = 100
sm = 30
padding = 10
symobl = "VIX"
# can get symbls like "MSFT" or "^VIX" (note the karat)
vix = get_symbol("^VIX")
print(f"SYMBOL: {json.dumps(vix.info,)}")
cur_price = vix.info.get('regularMarketPrice')
lst_price = vix.info.get('previousClose')

delta = (lst_price - cur_price) / cur_price
prcnt = round(delta * 100,2)
plus_minus = "-" if cur_price < lst_price else ""
prcnt_w_symbol = f"{plus_minus}{prcnt}%"
price = f"${cur_price}"


font = ImageFont.truetype(fnt, lg)
font_sm = ImageFont.truetype(fnt, sm)
im = Image.new("RGB", (500, 200), bg_clr)
d = ImageDraw.Draw(im)
w, h = d.textsize(symobl, font=font)
x = w * .75
y = h * 1.05 - 15
d.text((x,y), symobl, fill=tx_clr, anchor="ms", font=font)
d.text((x + padding, y+(sm + padding)), price, fill=tx_clr, anchor="ms", font=font_sm)
d.text((x + padding, y+((sm + padding) * 2)), prcnt_w_symbol, fill=tx_clr, anchor="ms", font=font_sm)

im.save("imgs/image.png")

