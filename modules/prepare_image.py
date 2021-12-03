from PIL import ImageFont
import textwrap


class PrepareImage():
    def __init__(self, processedData, common):
        self.__makeImage(common)
        self.max_price = processedData.max_price
        self.min_price = processedData.min_price
        self.__drawPriceLines(common, processedData)

        self.__makeDescription(common)


    def __makeImage(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw

        common.draw.rectangle((dw + drw, dh, w + dw + drw, h + dh), outline="black", width=2)

        for i in range(dw + drw, w + drw + dw + 1, common.left_indent):
            common.draw.line((i, h + dh - 1, i, h + dh + 3), fill="black")

    def __makeDescription(self, common):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        indicators_list, indicators_names = common.indicators_list, common.indicators_names

        f = ImageFont.load_default()
        offset_w = w + dw + 15
        offset_h = dh
        d = common.draw
        indent = 0
        color = 0
        for i in indicators_list:
            t = indicators_names[i]
            margin = 7
            d.rectangle((offset_w + 1, offset_h + indent + 4, offset_w + 4, offset_h + indent + 7),
                        fill=common.colors[color])
            for line in textwrap.wrap(t, width=11):
                d.text((offset_w + margin, offset_h + indent), line, font=f, fill=000)
                margin = 0
                indent += f.getsize(line)[1]
            color += 1
            indent += 5

    def __drawPriceLines(self, common, processedData):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        n = 15
        max_price = processedData.max_price
        min_price = processedData.min_price
        indent_px = h / n
        indent_money = (max_price - min_price) / n
        for i in range(n + 1):
            if not (i == 0 or i == n):
                common.draw.line((drw + dw + 2, dh + h - i * indent_px, drw + dw + w - 2, dh + h - i * indent_px),
                               fill="grey")
            common.draw.text((drw + 5, dh + h - i * indent_px), str(round(min_price + i * indent_money, 2)),
                           fill="black")
