
import os
import PIL
from PIL import Image, ImageDraw, ImageFont

from .tick_obj import TickObject


class TickerDetails(TickObject):    
    def __init__(self,symbol_data:any= None) -> None:
        super().__init__()
        # self.sm_font_size = 20
        self.current_symbol_data = symbol_data
    @classmethod
    def from_symbol(self,symbol:str):
        s = []
        s.append(symbol)
        t = TickerDetails()
        t.symbols = s 
        t.get_symbol_data(symbol=t.symbols[0])
        return t

    def refresh(self):
        
        font = ImageFont.truetype(self.font, self.sm_font_size)
        im = Image.new("L", (self.screen_width, self.screen_height), self.color_background)
        d = ImageDraw.Draw(im)
        padding =  15
        # data
        symbol = self._get_symbol()
        quote = self._get_quote()
        orig_symbol = symbol.replace("^","")
        info = quote.info
        # copy
        high = f"${info.get('fiftyTwoWeekHigh')}"
        low = f"${info.get('fiftyTwoWeekLow')}"
        msg = f"{orig_symbol}"
        
        # top line
        next_height,next_width = 0,10
        # d.text((next_width,next_height), msg, fill=self.color_text, font=font)
        # w_msg, h_msg = d.textsize(msg, font=font)        
        # next_height = next_height + h_msg 
        
        # high
        arrow = Image.open(os.path.join(self.directory_img, "arrow.png")).transpose(PIL.Image.ROTATE_180).resize((20,20))        
        arrow_x = next_width
        im.paste(arrow,(next_width, next_height + padding), mask=arrow)
        next_width = next_width + arrow.size[0] + padding        
        d.text((next_width ,next_height), high, fill=self.color_text,  font=font)

        # low
        w_high, h_high = d.textsize(high, font=font)
        next_height = next_height + h_high
        arrow = arrow.transpose(PIL.Image.ROTATE_180)
        im.paste(arrow,(arrow_x, next_height + padding), mask=arrow)
        next_width = arrow_x + arrow.size[0] + padding
        d.text((next_width,next_height), low, fill=self.color_text,  font=font)
        if self.epd :
            self.epd.Clear(0xFF)  
            if self.rotate_img:
                im = im.transpose(PIL.Image.ROTATE_180)
            self.epd.display_4Gray(self.epd.getbuffer_4Gray(im))
        else:
            im.save(os.path.join(self.directory_img, "details.png"), quality=95)
        