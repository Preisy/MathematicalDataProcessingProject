class ProcessDeltas:
    deltas = []
    par_all = True
    def __init__(self, common):
        self.deltas = []
        self.length = len(common.data)

    def overwrite(self):
        self.deltas = []
        self.length = 0

    def makeDeltas(self, data, same_extrema=False):
        if len(data) < self.length:
            data = [False for i in range(self.length - len(data))] + data

        diffs = []
        for i in range(1, len(data) - 1):
            if type(data[i - 1]) == type(False):
                diffs.append(0)
                continue
            if (data[i] - data[i - 1]) * (data[i + 1] - data[i]) < 0:
                if same_extrema:
                    diffs.append(True)
                else:
                    diffs.append(-1 if data[i] - data[i - 1] < 0 else 1)
            else:
                diffs.append(0)

        self.deltas.append(diffs)

    def analyseDeltas(self, common, analyze_data):
        w, dw, h, dh, drw = common.w, common.dw, common.h, common.dh, common.drw
        step_price, min_price = common.step_price, common.min_price

        deltas = []
        for i in range(len(self.deltas[0])):
            el = []
            for j in self.deltas:
                el.append(j[i])
            deltas.append(el)
        self.deltas = deltas

        left_indent = common.dw + common.left_indent
        for i in range(len(self.deltas)):
            ans = self.makeDecision(analyze_data, common.data[i + 1][5], i)
            color, flag = ans[0], ans[1]

            if flag:
                # left_indent += (i + 1) * common.left_indent

                common.draw.line(
                    (left_indent + common.left_indent / 2 + drw, dh,
                     left_indent + common.left_indent / 2 + drw, h + dh), fill=color)

            left_indent += common.left_indent

    k = 0

    def makeDecision(self, analyze_data, money, i):
        if i - analyze_data.region < 0:
            deltas = self.deltas[:i + 1]
        else:
            deltas = self.deltas[i - analyze_data.region: i + 1]

            if self.par_all:
                if all(i == 0 for i in deltas[analyze_data.region]):
                    analyze_data.append()
                    return [0, False]


        counter_list = [0, 0]
        length = len(deltas[0])
        for i in range(length):
            count = 0
            for j in deltas:
                if j[i] == -1:
                    counter_list[0] += 1
                elif j[i] == 1:
                    counter_list[1] += 1
                elif isinstance(j[i], type(True)):
                    counter_list[0] += 1
                    counter_list[1] += 1
        # print(counter_list)
        a = 0

        for j in range(len(counter_list)):
            if counter_list[j] / length >= 0.6:
                if j == 0:
                    analyze_data.buy(money)
                    # print(self.k, analyze_data.salary, analyze_data.purchase_amount)
                    # self.k += 1
                    return ["red", True]
                else:
                    analyze_data.sell(money)
                    # print(self.k, analyze_data.salary, analyze_data.purchase_amount)
                    # self.k += 1
                    return ["green", True]

        analyze_data.append()

        # flag = True
        # break
        return [0, False]