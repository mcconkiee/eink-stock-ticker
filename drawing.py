
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
# vix = get_symbol("^VIX")
# price = f"${vix.info.get('regularMarketPrice')}"
# print(f"SYMBOL: {json.dumps(vix.info)}")
price = "$30.11"

font = ImageFont.truetype(fnt, lg)
font_sm = ImageFont.truetype(fnt, sm)
im = Image.new("RGB", (500, 200), bg_clr)
d = ImageDraw.Draw(im)
w, h = d.textsize(symobl, font=font)
x = w * .75
y = h * 1.05
d.text((x,y), symobl, fill=tx_clr, anchor="ms", font=font)
d.text((x + padding, y+(sm + padding)), price, fill=tx_clr, anchor="ms", font=font_sm)

im.save("image.png")