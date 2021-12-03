from PIL import Image, ImageDraw


class DrawIndicators:
    indicators_constants = {
        "exp_N": 4,
        "moving_N": 5,
        "stdDev_N": 4,
        "rsi": 9,
        "uco": [1, 2 * 1, 4 * 1]
    }
    drawing_flag = True

    def __init__(self, common, makeDeltas, drawing_flag, par_stdDev_same_extra=True):
        # analysis parametres
        self.par_stdDev_same_extra = par_stdDev_same_extra

        self.drawing_flag = drawing_flag
        self.indicators = {
            1: self.__movingAverange,
            2: self.__expAverage,
            3: self.__standartDeviation,
            4: self.__accumulateSwingIndex,
            5: self.__relativeStrengthIndex,
            6: self.__ultimateOscillator
        }

        color = 0
        for i in common.indicators_list:
            args = self.indicators[i](common)


            if i == 3:
                if common.flag_delta:
                    # makeDeltas(args[1], True)
                    # makeDeltas(args[1], False)
                    makeDeltas(args[1], self.par_stdDev_same_extra)
            else:
                if common.flag_delta:
                    makeDeltas(args[1])

            if i in [3, 4, 5, 6]:
                self.__drawIndividualIndicator(common, common.colors[color], *args)
            else:
                self.__drawIndicator(common, common.colors[color], *args)
            color += 1

    def __movingAverange(self, common, N=-1):
        return_data = []
        if N == -1:
            N = self.indicators_constants["moving_N"]

        for i in range(len(common.data)):
            if i + 1 - N < 0:
                interval = [i[5] for i in common.data[:i + 1]]
            else:
                interval = [i[5] for i in common.data[i + 1 - N: i + 1]]

            average = sum(interval) / len(interval)
            return_data.append(average)


        return [0, return_data]

    def __expAverage(self, common, price_type=5, N=-1):
        if N == -1:
            N = self.indicators_constants["exp_N"]
        count = 0
        a = 2 / (N + 1)

        ema_prev = sum([i[price_type] for i in common.data[:N]]) / N
        return_data = []
        return_data.append(ema_prev)
        for i in common.data:
            if count < N:
                count += 1
                continue

            close = i[price_type]
            ema = a * close + (1 - a) * ema_prev

            return_data.append(ema)

            ema_prev = ema

        return [N - 1, return_data]
    def __expAverage_up(self, common, price_type=2, N=-1):
        if N == -1:
            N = self.indicators_constants["exp_N"]
        count = 0
        a = 2 / (N + 1)

        ema_prev = sum([i[price_type] for i in common.data[:N]]) / N
        return_data = []
        return_data.append(ema_prev)
        for i in common.data:
            if count < N:
                count += 1
                continue

            close = i[price_type]
            ema = a * close + (1 - a) * ema_prev

            return_data.append(ema)

            ema_prev = ema

        return [N - 1, return_data]

    def __standartDeviation(self, common):
        N = self.indicators_constants["stdDev_N"]

        return_data = []
        movingData = self.__movingAverange(common, N)[1]

        for i in range(len(common.data)):
            if i + 1 - N < 0:
                interval = [i[5] for i in common.data[:i + 1]]
            else:
                interval = [i[5] for i in common.data[i + 1 - N: i + 1]]

            stdDev = 0
            for j in range(len(interval)):
                if not ( type(interval[j]) == type(0.5) or type(interval[j]) == type(1) or type(movingData[i]) == type(0.5) or type(movingData[i]) == type(1)):
                    print(False)

                stdDev += (interval[j] - movingData[i]) ** 2

            stdDev = (stdDev / N) ** 0.5

            return_data.append(stdDev)

        return [0, return_data]

    def __accumulateSwingIndex(self, common):
        return_data = []

        asi = [0, 0]
        open = [0, 0]
        close = [0, 0]
        high = [0, 0]
        low = [0, 0]

        for i in range(len(common.data)):
            if i == 0:
                open[0] = common.data[i][2]
                close[0] = common.data[i][5]
                high[0] = common.data[i][3]
                low[0] = common.data[i][4]
                continue
            open[1] = common.data[i][2]
            close[1] = common.data[i][5]
            high[1] = common.data[i][3]
            low[1] = common.data[i][4]

            # tr = max(high[1] - close[0], low[1] - close[0], high[1] - low[1])
            # if close[0] > high[1]:
            #     er = high[1] - close[0]
            # elif low[1] <= close[0] <= high[1]:
            #     er = 0
            # elif close[0] < low[1]:
            #     er = low[1] - close[0]
            # sh = close[0] - open[0]

            arr = [abs(high[1] - close[0]), abs(low[1] - close[0]), abs(high[1] - low[1])]
            arr_index = arr.index(max(arr))
            if arr_index == 0:
                r = abs(high[1] - close[0]) - 0.5 * abs(low[1] - close[0]) + 0.25 * abs(close[0] - open[0])
            elif arr_index == 1:
                r = abs(low[1] - close[0]) - 0.5 * abs(high[1] - close[0]) + 0.25 * abs(close[0] - open[0])
            elif arr_index == 2:
                r = abs(high[1] - low[1]) + 0.25 * abs(close[0] - open[0])


            # r = tr - 0.5 * er + 0.25 * sh

            k = max(abs(high[1] - close[0]), abs(low[1] - close[0]))
            t = 3

            # print(close[1] - close[0] + 0.5 * (close[1] - open[1]) + 0.25 * (close[0] - open[0]))
            # print(k)
            # print(r)
            # print(t)
            si = 50 * ((close[1] - close[0] + 0.5 * (close[1] - open[1]) + 0.25 * (close[0] - open[0])) / r) * k / t
            # print(si)

            asi[1] = asi[0] + si

            return_data.append(asi[1])
            # print(asi[1])

            asi[0] = asi[1]
            open[0] = open[1]
            close[0] = close[1]
            high[0] = high[1]
            low[0] = low[1]

        return [1, return_data]

    # def __accumulateSwingIndex(self, common):
    #
    #     return_data = []
    #
    #     asi = [0, 0]
    #     open = [0, 0]
    #     close = [0, 0]
    #     high = [0, 0]
    #     low = [0, 0]
    #
    #     for i in range(len(common.data)):
    #         if i == 0:
    #             open[0] = common.data[i][2]
    #             close[0] = common.data[i][5]
    #             high[0] = common.data[i][3]
    #             low[0] = common.data[i][4]
    #             continue
    #         open[1] = common.data[i][2]
    #         close[1] = common.data[i][5]
    #         high[1] = common.data[i][3]
    #         low[1] = common.data[i][4]
    #
    #         tr = max(high[1] - close[0], low[1] - close[0], high[1] - low[1])
    #         if close[0] > high[1]:
    #             er = high[1] - close[0]
    #         elif low[1] <= close[0] <= high[1]:
    #             er = 0
    #         elif close[0] < low[1]:
    #             er = low[1] - close[0]
    #         sh = close[0] - open[0]
    #
    #         r = tr - 0.5 * er + 0.25 * sh
    #
    #         k = max(high[0] - close[1], low[0] - close[1])
    #         t = 11
    #
    #         si = 50 * ((close[0] - close[1] + 0.5 * (close[0] - open[0]) + 0.25 * (close[1] - open[1])) / r) * k / t
    #
    #         asi[1] = asi[0] + si
    #
    #         return_data.append(asi[1])
    #         # print(asi[1])
    #
    #         asi[0] = asi[1]
    #         open[0] = open[1]
    #         close[0] = close[1]
    #         high[0] = high[1]
    #         low[0] = low[1]
    #
    #
    #
    #     return [1, return_data]

    def __relativeStrengthIndex(self, common):
        N = self.indicators_constants["rsi"]

        return_data = []

        for i in range(N - 1, len(common.data)):
            if i + 1 - N < 0:
                interval = [[i[2], i[5]] for i in common.data[:i + 1]]
            else:
                interval = [[i[2], i[5]] for i in common.data[i + 1 - N: i + 1]]

            cu, cd = 0, 0
            for j in interval:
                if j[0] - j[1] > 0:
                    cu += j[0] - j[1]
                else:
                    cd += j[1] - j[0]
            cu /= len(interval)
            cd /= len(interval)


            if cu == 0:
                rs = 0
            else:
                rs = cd / cu

            return_data.append(100 - 100 / (1 + rs))

        return [N - 1, return_data]

    def __ultimateOscillator(self, common):
        N = self.indicators_constants["uco"]

        return_data = []

        buying_pressure_arr = []
        true_range_arr = []

        for i in range(len(common.data)):
            close = [common.data[i - 1][5], common.data[i][5]]
            low = common.data[i][4]
            buying_pressure = close[1] - min(low, close[0])
            buying_pressure_arr.append(buying_pressure)

            high = common.data[i][3]
            true_range = max(high - low, high - close[0], close[0] - low)
            true_range_arr.append(true_range)
            if not max(high - low, high - close[0], close[0] - low) == max(high, close[0]) - min(low, close[0]):
                print("ss")

            if i + 1 < N[2]:
                continue
            totalBuyingPressure_short = sum(buying_pressure_arr[i + 1 - N[0]: i + 1])/sum(true_range_arr[i + 1 - N[0]: i + 1])
            totalBuyingPressure_medium = sum(buying_pressure_arr[i + 1 - N[1]: i + 1])/sum(true_range_arr[i + 1 - N[1]: i + 1])
            totalBuyingPressure_long = sum(buying_pressure_arr[i + 1 - N[2]: i + 1])/sum(true_range_arr[i + 1 - N[2]: i + 1])

            uo = 100 * (4 * totalBuyingPressure_short + 2 * totalBuyingPressure_medium + totalBuyingPressure_long) / (4 + 2 + 1)

            return_data.append(uo)

        return [N[2] - 1, return_data]



    def __drawIndicator(self, common, color, start_count, data):
        if not self.drawing_flag:
            return
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        step_price, min_price = common.step_price, common.min_price
        left_indent = dw
        left_indent += common.left_indent * (start_count)

        for i in range(len(data)):
            if i == 0:
                prev_el = data[i]
                left_indent += common.left_indent
                continue

            current_el = data[i]

            common.draw.line(
                (left_indent + drw - common.left_indent / 2,
                 h + 1 - step_price * (prev_el - min_price) + dh,
                 left_indent + drw + common.left_indent / 2,
                 h + 1 - step_price * (current_el - min_price) + dh), fill=color, width=2)

            prev_el = current_el
            left_indent += common.left_indent

    def __drawIndividualIndicator(self, common, color, start_count, data):
        if not self.drawing_flag:
            return
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        indicatorH = common.individual_indicator_h
        min_value = min(data)
        max_value = max(data)
        step_value = indicatorH / (max_value - min_value)

        size = common.image.size
        new_image = Image.new("RGB", (size[0], size[1] + indicatorH + dh), color="white")

        new_image.paste(common.image)
        common.image = new_image
        common.draw = ImageDraw.Draw(common.image)

        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        n = 5
        indent_px = indicatorH / n
        indent_money = (max_value - min_value) / n

        zero_h = (indicatorH / (max_value - min_value)) * abs(min_value)

        common.draw.line((drw + dw + 2, size[1] + indicatorH - zero_h, drw + dw + w - 2,
                          size[1] + indicatorH - zero_h),
                         fill="black")

        common.draw.text((drw + 5, size[1] + indicatorH - zero_h), str(0),
                     fill="black")

        for i in range(n + 1):
            if not (i == 0 or i == n):
                common.draw.line((drw + dw + 2, size[1] + indicatorH - i * indent_px, drw + dw + w - 2, size[1] + indicatorH - i * indent_px),
                               fill="grey")
            common.draw.text((drw + 5, size[1] + indicatorH - i * indent_px), str(round(min_value + i * indent_money, 2)),
                           fill="black")


        common.draw.rectangle((dw + drw, size[1], w + dw + drw, size[1] + indicatorH), outline="black", width=2)

        left_indent = dw
        left_indent += common.left_indent * (start_count)

        for i in range(len(data)):
            if i == 0:
                prev_el = data[i]
                left_indent += common.left_indent
                continue

            current_el = data[i]

            common.draw.line(
                (left_indent + drw - common.left_indent / 2, size[1] + indicatorH - step_value * (prev_el - min_value),
                 left_indent + drw + common.left_indent / 2, size[1] + indicatorH - step_value * (current_el - min_value)), fill=color, width=2)

            prev_el = current_el
            left_indent += common.left_indent
