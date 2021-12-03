class PrepareData:
    titleDates = [-1, -1]
    def __init__(self, periodicity, dates):
        self.periodicity = periodicity
        self.dates = dates
        self._PrepareData__readData()
        self._PrepareData__describeData()

    def __readData(self):
        file = open("YNDX_180311_200311.txt", "r")
        file.readline()
        data = []

        eq = 0
        if self.periodicity == 1:
            eq = 4 + 2 + 2
        elif self.periodicity == 2:
            eq = 4 + 2
        elif self.periodicity == 3:
            eq = 4

        if self.dates == [-1, -1]:
            value = file.readline()
            value = list(map(float, value.split(";")[1:]))[1:7]
            value[0] = float(str(value[0])[:eq + 2])
            prev_value = value[0]
        else:
            # <DATE>;  <TIME>;<OPEN>;      <HIGH>;      <LOW>;      <CLOSE>
            # 20180312;110000;2465.0000000;2469.0000000;2445.0000000;2458.0000000
            value = [0, 0, 0, 0, float("inf"), 0]
            prev_value = value[0]



        if eq == 8:
            arr = value.copy()
        else:
            arr = [value[0], 0, 0, 0, float("inf"), 0]

        arr[2] = value[2]
        for line in file:
            value = list(map(float, line.split(";")[1:]))[1:7]
            if not self.dates[0] == -1:
                arr = value.copy()
                arr[0] = float(str(value[0])[:eq + 2])
                if eq == 8:
                    arr[1] = value[1]
                else:
                    arr[1] = 0
                prev_value = value[0]
                if self.dates[0] <= value[0]:
                    self.dates[0] = -1
                    if self.titleDates[0] == -1:
                        self.titleDates[0] = float(str(value[0])[:eq + 2])
                    file.readline()
                else:
                    continue
            elif self.titleDates[0] == -1:
                    self.titleDates[0] = float(str(value[0])[:eq + 2])

            if eq == 8:
                data.append(value.copy())
            elif str(value[0])[eq:eq + 2] == str(prev_value)[eq:eq + 2] and not eq == 8:
                arr[3] = max(arr[3], value[3])
                arr[4] = min(arr[4], value[4])
                arr[5] = value[5]
            else:
                data.append(arr.copy())
                prev_value = value[0]
                arr[0] = float(str(value[0])[:eq + 2])
                if eq == 8:
                    arr[1] = value[1]
                arr[2] = value[2]
                arr[3] = value[3]
                arr[4] = value[4]
                arr[5] = value[5]
            if not self.dates[1] == -1:
                if self.dates[1] < value[0]:
                    break

            self.titleDates[1] = float(str(value[0])[:eq + 2])
        self.data = data

    def __describeData(self):
        max_price = self.data[0][2]
        min_price = self.data[0][2]
        for i in self.data:
            min_price = min(min_price, *i[2:5])
            max_price = max(max_price, *i[2:5])
        self.max_price, self.min_price = max_price, min_price