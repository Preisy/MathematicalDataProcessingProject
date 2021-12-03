from PIL import Image, ImageDraw
class Common:
    drw = 5
    colors = ["blue", "orange", "#ef00ff", "#ff6262", "#540055", "#009f05"]
    indicators_names = {
        1: "Moving average",
        2: "Exponential average",
        3: "Standard Deviation",
        4: "Accumulate Swing Index",
        5: "Relative Strength Index",
        6: "Ultimate Oscillator"
    }
    h = 600
    individual_indicator_h = 150
    left_indent = 10
    flag_delta = True


    def __init__(self, dw, dh, processedData, indicators_list, periodicity):
        self.data = processedData.data
        self.min_price, self.max_price = processedData.min_price, processedData.max_price
        self.dw = dw
        self.dh = dh
        self.w = (len(self.data)) * self.left_indent
        self.h = 800
        self.step_price = self.h / (processedData.max_price - processedData.min_price)

        self.indicators_list = indicators_list

        indent_for_dates = 0
        if periodicity == 1:
            indent_for_dates = 95
        elif periodicity == 2:
            indent_for_dates = 59
        elif periodicity == 3:
            indent_for_dates = 41


        self.image = Image.new("RGB",
                               (self.w + 2 * self.dw + self.drw + 50, self.h + 2 * self.dh + indent_for_dates),
                               color="white")
        print(self.w + 2 * self.dw, self.h + 2 * self.dh)
        self.draw = ImageDraw.Draw(self.image)