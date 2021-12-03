import os

from modules.console_manager import ConsoleManager
from modules.common import Common
from modules.prepare_data import PrepareData
from modules.prepare_image import PrepareImage
from modules.draw_candles_with_dates import CandlesAndDates
from modules.process_deltas import ProcessDeltas
from modules.technical_analysis_indicators import DrawIndicators
from modules.analyze_data import AnalyzeData
from modules.print_salary import PrintSalary

# <DATE>;  <TIME>;<OPEN>;      <HIGH>;      <LOW>;      <CLOSE>
# 20180312;110000;2465.0000000;2469.0000000;2445.0000000;2458.0000000

# error
# 2019.03.25 - 2019.03.27
# 1

# название временной_промежуток шаг_по_времени

# использовать метод экстраполяции
# сделать прогноз на несколько временных шагов
# arima
# сделать самому и найти библиотеку. сравнить
# arima - авторегрессионная модель
# линейная регрессия - одно значение линейно зависит от остальных
# авторегрессия - слудующая цена зависит от предыдщуих
# подобрать коэффициенты

# метод наименьших квадратов


# в какой области работаем
# что в нкй есть
# в чем она несовершенна
# что я могу предложить
# что я реализовал
# описать то, что получилось в результате

def makeDateFormat(el):
    el = str(int(el))
    if len(el) == 8:
        el = f"{el[:4]}.{el[4:6]}.{el[6:]}"
    elif len(el) == 6:
        el = f"{el[:4]}.{el[4:6]}"

    return el

console = ConsoleManager()
if console.flag:
    processedData = PrepareData(console.periodicity, console.dates)

    title = f"graph {makeDateFormat(processedData.titleDates[0])}-{makeDateFormat(processedData.titleDates[1])} "
    if console.periodicity == 1:
        title += "hour"
    elif console.periodicity == 2:
        title += "day"
    elif console.periodicity == 3:
        title += "month"

    common = Common(50, 20, processedData, console.indicators, console.periodicity)

    processedImage = PrepareImage(processedData, common)

    candles = CandlesAndDates(common)

    deltas = ProcessDeltas(common)
    techAnalysis = DrawIndicators(common, deltas.makeDeltas, True)

    if common.flag_delta and not common.indicators_list == []:
        analyze_data = AnalyzeData()
        deltas.analyseDeltas(common, analyze_data)
        analyze_data.total()

        print_salary = PrintSalary(common, analyze_data)

    print(len(common.data))

    os.makedirs("images", exist_ok=True)
    common.image.save(f"images/{title}.png", "PNG")
