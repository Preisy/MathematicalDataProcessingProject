from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps

class CandlesAndDates():
    def __init__(self, common):
        self.max_price, self.min_price = common.max_price, common.min_price
        self.__drawCandles(common)

    def __intermediateImage(self, i):
        f = ImageFont.load_default()
        text_width = 95
        if i[1] == 0:
            if len(str(int(i[0]))) == 6:
                text = f'{str(i[0])[:4]}.{str(i[0])[4:6]}'
                text_width -= 54
            else:
                text = f'{str(i[0])[:4]}.{str(i[0])[4:6]}.{str(i[0])[6:8]}'
                text_width -= 36
        else:
            text = f'{str(i[0])[:4]}.{str(i[0])[4:6]}.{str(i[0])[6:8]} {str(i[1])[:2]}:{str(i[1])[2:4]}'

        txt = Image.new('L', (text_width, 7))
        d = ImageDraw.Draw(txt)
        d.text((0, -2), text, font=f, fill=255)
        p = txt.rotate(90, expand=1)
        # txt.save("1.png", "PNG")
        return p

    def __drawCandles(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        step_price, min_price = common.step_price, common.min_price

        left_indent = dw
        for i in common.data:
            open, high, low, close = i[2], i[3], i[4], i[5]
            if open - close > 0:
                bg_color = "black"
                outline_color = "black"
            else:
                bg_color = "white"
                outline_color = "black"
            common.draw.rectangle(
                (left_indent + 2 + drw,
                 h - step_price * (open - min_price) + dh,
                 left_indent + common.left_indent - 2 + drw,
                 h - step_price * (close - min_price) + dh),
                fill=bg_color, outline=outline_color)
            common.draw.line(
                (left_indent + common.left_indent / 2 + drw,
                 h - step_price * (high - min_price) + dh,
                 left_indent + common.left_indent / 2 + drw,
                 h - step_price * (low - min_price) + dh),
                fill="black")

            p = self.__intermediateImage(i)
            # p.save("1.png", "PNG")

            common.image.paste(ImageOps.colorize(p, (0, 0, 0), (0, 0, 0)), (left_indent + int(common.left_indent / 2 - 3.5) + drw, h + dh + 5), p)
            left_indent += common.left_indent
