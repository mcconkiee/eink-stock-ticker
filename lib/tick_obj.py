from .chart import quickchart
from .symbol import get_history, get_symbol
from .iex import fetch_quote
from time import time, sleep
from .tickers import Tickers

from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
import PIL
import logging
import json
from mimetypes import init
import sys
import os
srcdir = os.path.dirname(os.path.realpath(__file__))
fontdir = os.path.join(srcdir, "../fonts")
imgsdir = os.path.join(srcdir, "../imgs")


SLEEPTIME = 25
HAS_EPD = False
if os.path.exists('/sys/'):
    HAS_EPD = True
    from .epd2in7 import EPD

# configs
FWD = 5
DETAILS = 6
RESET = 19
VIX = 13
chart_clr = 0xaa  # https://www.color-hex.com
tx_clr = 0  # text color
bg_clr = 255  # white background

fnt = os.path.join(fontdir, 'Arial Black.ttf')


class TickObject:
    epd = None
    btn1 = None
    btn2 = None
    btn3 = None
    btn4 = None
    logging.basicConfig(level=logging.INFO)
    symbols: list[str] = []

    # these are flipped on purpose
    rotate_img = False
    screen_width = 264
    screen_height = 176
    font = fnt
    lg_font_size = 15  # large font
    sm_font_size = 10  # small font
    padding = 0
    counter = 0  # increment/decrement on each cycle
    idx = 0  # keeps reference in our  tiker index
    increment = 1  # direction + || -
    color_background = bg_clr
    color_text = tx_clr
    current_symbol_data = None
    directory_font = fontdir
    directory_img = imgsdir
    def __init__(self) -> None:
        if HAS_EPD:
            # setup epd
            _epd = EPD()  # get the display
            self.screen_width = _epd.height
            self.screen_height = _epd.width
            _epd.Init_4Gray()           # initialize the display
            # prints to console, not the display, for debugging
            logging.info("Clear display")
            _epd.Clear(0xFF)
            self.epd = _epd
            self.btn1 = Button(FWD)
            self.btn2 = Button(DETAILS)
            self.btn3 = Button(VIX)
            self.btn4 = Button(RESET)
            self.btn1.when_pressed = self.handleBtnPress
            self.btn2.when_pressed = self.handleBtnPress
            self.btn3.when_pressed = self.handleBtnPress
            self.btn4.when_pressed = self.handleBtnPress

        self.lg_font_size = int(self.screen_height/2)  # large font
        self.sm_font_size = int(self.screen_height/8)  # small font
        self.symbols = self.get_tickers()
    def get_symbol_data(self,symbol:str):
        self.current_symbol_data = get_symbol(symbol=symbol)
        return self.current_symbol_data
    def _get_quote(self):
        return self.current_symbol_data

    def _get_symbol(self):
        return self._get_quote().info.get('symbol')

    def update_msgs(self, msg: str, submsg: str = None, subsubmsg: str = None, display: bool = False, x: float = None, y: float = None):
        font = ImageFont.truetype(fnt, self.lg_font_size if len(
            msg) <= 3 else int(self.lg_font_size * .75))
        font_sm = ImageFont.truetype(fnt, self.sm_font_size)
        im = Image.new("L", (self.screen_width, self.screen_height), bg_clr)
        d = ImageDraw.Draw(im)
        w, h = d.textsize(msg, font=font)

        if x == None:
            x = self.screen_width/2  # 0 = left, width = right
        if y == None:
            y = self.screen_height - 30  # 0 = top, height = bottom

        d.text((x, y), msg, fill=tx_clr, anchor="ms", font=font)
        if submsg:
            d.text((x + self.padding, y+(self.sm_font_size + self.padding)),
                   submsg, fill=tx_clr, anchor="ms", font=font_sm)
        if subsubmsg:
            d.text((x + self.padding, y+((self.sm_font_size + self.padding)
                                         * 2)), subsubmsg, fill=tx_clr, anchor="ms", font=font_sm)
        
            
        if self.epd and display:
            self.epd.Clear(0xFF)
            if self.rotate_img:
                im = im.transpose(PIL.Image.ROTATE_180)
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(im))
        return im

    def display_symbol(self):
        quote = self._get_quote()
        symbol = self._get_symbol()
        orig_symbol = symbol.replace("^", "")

        history = get_history(symbol=symbol)

        # remove the karat if we have one (eg ^VIX)
        symbol = orig_symbol
        # print(f"SYMBOL: {json.dumps(quote.info)}")
        cur_price = float(quote.info.get('regularMarketPrice'))
        lst_price = float(quote.info.get('previousClose'))

        is_up = cur_price > lst_price
        price_diff = float(
            cur_price - lst_price) if is_up else float(lst_price - cur_price)
        price_diff = round(price_diff, 2)

        delta = price_diff / cur_price
        prcnt = round(delta * 100, 2)
        plus_minus = "-" if not is_up else "+"
        prcnt_w_symbol = f"{plus_minus}{price_diff} {plus_minus}{prcnt}%"
        # price = f"${cur_price} (${lst_price})"
        price = f"${cur_price}"
        logging.info(f"{symbol} @  ${price} {prcnt_w_symbol}")

        
        # get prices to understand where is the chart line
        first_price = history["Open"][0]
        last_price = history["Open"][-1]
        length = history["Open"].shape[0]
        mid_price_idx = round(length/2)
        mid_price = history["Open"][mid_price_idx]
        # yvalue = (30 if mid_price < first_price  else height - 40)
        im = self.update_msgs(msg=symbol, submsg=price,
                              subsubmsg=prcnt_w_symbol, y=100)
        
        # DRAW high/low
        # hilow = Image.new("L", (self.screen_width, self.screen_height), bg_clr)
        d = ImageDraw.Draw(im)
        detail_size = 15
        font = ImageFont.truetype(self.font, detail_size)         
        next_width,next_height = 10,10
        high = f"${self.current_symbol_data.info.get('fiftyTwoWeekHigh')}"
        low = f"${self.current_symbol_data.info.get('fiftyTwoWeekLow')}"
        # high
        arrow = Image.open(os.path.join(self.directory_img, "arrow.png")).transpose(PIL.Image.ROTATE_180).resize((detail_size,detail_size))        
        arrow_x = next_width
        im.paste(arrow,(next_width, next_height), mask=arrow)
        next_width = next_width + arrow.size[0] + self.padding        
        d.text((next_width ,next_height-2), high, fill=self.color_text,  font=font)

        # low
        w_high, h_high = d.textsize(high, font=font)
        arrow = arrow.transpose(PIL.Image.ROTATE_180)
        next_width = self.screen_width - (w_high + self.padding + arrow.size[0])
        im.paste(arrow,(next_width - 15, next_height + 3), mask=arrow)
        next_width = next_width + self.padding        
        d.text((next_width ,next_height), low, fill=self.color_text,  font=font)
        # create chart
        chart_img = quickchart(
            width=int(self.screen_width/2),
            height=int(self.screen_height/2),
            dataset=history["Open"],
            background_clr=f"rgb({bg_clr},{bg_clr},{bg_clr})",
            line_clr=f"rgb({chart_clr},{chart_clr},{chart_clr})",
            saved_image_path=os.path.join(imgsdir, "chart.png"))
        # get chart image
        # flip this image since we want the powersource on the bottom

        chart = Image.open(os.path.join(
            imgsdir, "chart.png"))  # .convert("RGBA")
        back_im = im.copy()
        if self.rotate_img:
            chart = chart.transpose(PIL.Image.ROTATE_180)
            back_im = back_im.transpose(PIL.Image.ROTATE_180)
        
        back_im.paste(chart, (1, 1), mask=chart)
        
        back_im.save(os.path.join(imgsdir, "quote.png"), quality=95)

        back_im.save(os.path.join(imgsdir, f"{symbol}.png"), quality=95)

        logging.info(f"Display quote {symbol}")
        if self.epd:
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(back_im))

    def get_tickers(self):
        t = Tickers()
        data = t.get_tickers()
        return data['tickers']

    def refresh(self):
        size = len(self.symbols)
        sleep_time = SLEEPTIME
        logging.info(
            f"symbols at refresh = {self.symbols}: idx = {self.idx} : counter = {self.counter}")
        symbol = self.symbols[self.idx]
        logging.info(f"{symbol}••")
        try:
            quote = self.get_symbol_data(symbol=symbol)
            self.current_symbol_data = quote
            self.display_symbol()
        except Exception as error:
            logging.error(f"error on symbol {symbol}")
            logging.critical(error)
            sleep_time = 10
        self.counter = (self.counter + self.increment)
        self.idx = self.counter % size
        sleep(sleep_time - time() % sleep_time)



    def tick(self, loop=True):
        self.refresh()        

    # https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8
    # https://gist.github.com/RaneWallin/fd73ddbffdabea23358f722adb9f4075

    def handleBtnPress(self, btn):

        if HAS_EPD:
            self.epd.Clear(0xFF)
            pinNum = btn.pin.number
            if pinNum == VIX:
                self.counter = 0
                self.idx = 0
                self.symbols = ["^VIX"]
            else:
                if pinNum == FWD:
                    self.increment = self.increment + 1
                if pinNum == DETAILS:
                    return
                if pinNum == RESET:
                    self.rotate_img = not self.rotate_img
                    self.increment = 1
                    self.counter = 0

            size = len(self.symbols)
            self.counter = (self.counter + self.increment)
            self.idx = self.counter % size

        self.refresh()
        if size == 1:
            self.symbols = self.get_tickers()
