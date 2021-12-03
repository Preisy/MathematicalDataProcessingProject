import re


class ConsoleManager:
    periodicity = 0
    indicators = []
    answer = 0
    flag = True
    dates = [-1, -1]

    def __init__(self):
        self.__periodicityAnswer()

    def __periodicityAnswer(self):
        print("---------------------------------------")
        print("Выберите периодичность вывода данных:")
        print("Час (не оптимально) - 1")
        print("День - 2")
        print("Месяц - 3")
        print("Указать промежуток выбора - 4")
        print("Указать дефолтное значение - 5")
        print()
        print("Выход - 0")
        print("---------------------------------------")
        answer = input()
        if not answer in map(str, range(0, 9 + 1)):
            print("Неккоректный формат ввода данных")
            self.__periodicityAnswer()
            return

        answer = int(answer)
        if not answer in range(0, 5 + 1):
            print("Неверное значение")
            self.__periodicityAnswer()
            return

        if answer == 0:
            self.flag = False
            return
        if answer == 4:
            self.__outputInterval()
            return

        if answer == 5:
            # self.dates = [20180312.0, 20180820.0]
            # self.periodicity = 2
            # self.dates = [20190506.0, 20190530.0]
            # self.periodicity = 1
            self.dates = [20191011.0, 20200311.0]
            self.periodicity = 2

            # long time periods
            # self.dates = [20180312.0, 20180520.0]
            # self.periodicity = 1
            # self.dates = [20190312.0, 20190520.0]
            # self.periodicity = 1
            # self.dates = [20191212.0, 20200311.0]
            # self.periodicity = 1

            self.__indicatorsAnswer()
            return

        self.periodicity = answer

        self.__indicatorsAnswer()

    def __outputInterval(self):
        print("---------------------------------------")
        print("Введите две даты: начало и конец вывода\nВ формате 2018.03.12 - 2019.03.12")
        print("Вторым вводимым числом укажите периодичность вывода данных:")
        print("Час - 1")
        print("День - 2")
        print("Месяц - 3")
        print()
        print("Назад - 0")
        print("---------------------------------------")

        dates = input()
        if dates == "0":
            self.__periodicityAnswer()
            return
        if re.match(r'\d{4}\.\d{2}\.\d{2}\s\-\s\d{4}\.\d{2}\.\d{2}', dates) == None:
            print("Неккоректный формат ввода данных")
            self.__outputInterval()
            return
        dates = [float("".join(i.split("."))) for i in dates.split(" - ")]
        answer = int(input())
        if not answer in range(0, 3 + 1):
            print("Неверное значение")
            self.__outputInterval()
            return

        self.dates = dates
        self.periodicity = answer

        self.__indicatorsAnswer()

    def __indicatorsAnswer(self):
        print("---------------------------------------")
        print("Выберите индикаторы технического анализа:")
        print("Скользящее среднее - 1")
        print("Экспоненциальное среднее - 2")
        print("Стандартное отклонение - 3")
        print("Куммулятивный индекс колебаний - 4")
        print("Индекс относительной силы - 5")
        print("Окончательный осциллятор - 6")

        print("Принять - y")
        print()
        print("Назад - 0")
        print("---------------------------------------")
        answer = input()

        if answer == "y":
            return

        amount_indicators = 6

        if (not answer == "y" and not answer in map(str, range(0, amount_indicators + 1))) or int(answer) in self.indicators:
            print("Неверное значение")
            self.__indicatorsAnswer()
            return
        if int(answer) == 0:
            self.indicators = []
            self.__periodicityAnswer()
            return

        if int(answer) in range(1, amount_indicators + 1):
            self.indicators.append(int(answer))
            if not len(self.indicators) == amount_indicators:
                self.__indicatorsAnswer()
