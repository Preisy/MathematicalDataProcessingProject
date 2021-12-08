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

from itertools import combinations


console = ConsoleManager()
if console.flag:


    processedData = PrepareData(console.periodicity, console.dates)

    common = Common(50, 20, processedData, console.indicators, console.periodicity)

    def line(tup, fill=""):
        return
    common.draw.line = line


    analyze_data = AnalyzeData()

    file = open("result.txt", "w")

    # for j in range(3):
    for i in range(2**9 + 1, 2**9 * 2):
        ind = []
        par_arr = list(map(int, list(bin(i)[2:])))[1:]

        par_region = par_arr[0]
        par_all = bool(par_arr[1])
        par_stdDev_same_extra = bool(par_arr[2])
        n = par_arr[3:]


        # n = par_arr
        for j in range(len(n)):
            if n[j] == 1:
                ind.append(j + 1)

        if all(i == 0 for i in n):
            # file.write(' '.join(map(str, par_arr)) + " " + "0\n")
            file.write("0\n")
            continue

        # parametres
        common.indicators_list = ind
        analyze_data.region = par_region

        deltas = ProcessDeltas(common)

        # parametres
        deltas.par_all = par_all

        techAnalysis = DrawIndicators(common, deltas.makeDeltas, False, par_stdDev_same_extra)

        # если оставить analyze_data здесь, то нет перезаписи свойств analyze_data. те сохраняются history_salary и тд
        # analyze_data = AnalyzeData()
        deltas.analyseDeltas(common, analyze_data)

        # file.write(' '.join(map(str, par_arr)) + " " + str(round(analyze_data.salary)) + "\n")
        file.write(str(round(analyze_data.salary)) + "\n")

        analyze_data.overwrite()

    print(len(common.data))

    os.makedirs("images", exist_ok=True)
    common.image.save(f"images/test.png", "PNG")

