# -*- coding: utf-8 -*-
import random
import math

import pylab

import bee
import beeExamples
import beePlotting
import PySimpleGUI as gui

if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Оптимизация пчелиным роем", justification='center', size=(50, 1), font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Число пчел-разведчиков:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(300, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число пчел на выбранных участках:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(10, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число пчел на лучших участках:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(30, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число перспективных участков:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(15, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число лучших участков:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(5, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число запусков алгоритма:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(1, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Максимальное число итераций:", font=('ComicSans', 12), size=(29, 1)), gui.InputText(2000, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Предельное число итераций без улучшения решения:", font=('ComicSans', 12), size=(43, 1)), gui.InputText(10, font=('ComicSans', 12), size=(10, 1))],
        [gui.Radio("Функция Сферы", "Radio1", default=True, key="Sphere", font=('ComicSans', 12)),
         gui.Radio("Функция De Jong", "Radio1", default=False, key="Jong", font=('ComicSans', 12)),
         gui.Radio("Функция Goldstein", "Radio1", default=False, key="Goldstein", font=('ComicSans', 12))],
        [gui.Radio("Функция Розенброка", "Radio1", default=False, key="Rosenbrock", font=('ComicSans', 12)),
         gui.Radio("Функция тестовая", "Radio1", default=False, key="Test", font=('ComicSans', 12)),
         gui.Radio("Функция степенная", "Radio1", default=False, key="Func", font=('ComicSans', 12))],
        [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Оптимизация пчелиным роем', layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        ###################################################
        ##                     Параметры алгоритма
        ###################################################

        if event == 'Вычислить':
            # Количество пчел-разведчиков
            scoutbeecount = int(values[0])
            # Количество пчел, отправляемых на выбранные, но не лучшие участки
            selectedbeecount = int(values[1])
            # Количество пчел, отправляемые на лучшие участки
            bestbeecount = int(values[2])
            # Количество выбранных, но не лучших, участков
            selsitescount = int(values[3])
            # Количество лучших участков
            bestsitescount = int(values[4])
            # Количество запусков алгоритма
            runcount = int(values[5])
            # Максимальное количество итераций
            maxiteration = int(values[6])
            # Через такое количество итераций без нахождения лучшего решения уменьшим область поиска
            max_func_counter = int(values[7])

            # Класс пчел, который будет использоваться в алгоритме
            if values["Sphere"] == True:
                beetype = beeExamples.spherebee
            elif values["Jong"]:
                beetype = beeExamples.dejongbee
            elif values["Goldstein"]:
                beetype = beeExamples.goldsteinbee
            elif values["Rosenbrock"]:
                beetype = beeExamples.rosenbrockbee
            elif values["Test"]:
                beetype = beeExamples.testbee
            elif values["Func"]:
                beetype = beeExamples.funcbee

            # Включаем интерактивный режим
            pylab.ion()

            # Будем сохранять статистику
            stat = bee.statistic()

            # Имя файла для сохранения статистики
            stat_fname = "stat/beestat_%s.txt"

            # Во столько раз будем уменьшать область поиска
            koeff = beetype.getrangekoeff()

            ###################################################

            for runnumber in range(runcount):
                currhive = bee.hive(scoutbeecount, selectedbeecount, bestbeecount, \
                                    selsitescount, bestsitescount, \
                                    beetype.getstartrange(), beetype)

                # Начальное значение целевой функции
                best_func = -1.0e9

                # Количество итераций без улучшения целевой функции
                func_counter = 0

                stat.add(runnumber, currhive)

                for n in range(maxiteration):
                    currhive.nextstep()

                    stat.add(runnumber, currhive)

                    if currhive.bestfitness != best_func:
                        # Найдено место, где целевая функция лучше
                        best_func = currhive.bestfitness
                        func_counter = 0

                        # Обновим рисунок роя пчел
                        beePlotting.plotswarm (currhive, 0, 1)

                        # print("\n*** iteration %d / %d" % (runnumber + 1, n))
                        # print("Best position: %s" % (str(currhive.bestposition)))
                        # print("Best fitness: %f" % currhive.bestfitness)
                    else:
                        func_counter += 1
                        if func_counter == max_func_counter:
                            # Уменьшим размеры участков
                            currhive.range = [currhive.range[m] * koeff[m] for m in range(len(currhive.range))]
                            func_counter = 0

                    print("\n*** iteration %d / %d (new range)" % (runnumber + 1, n))
                    print("New range: %s" % (str(currhive.range)))
                    print("Best position: %s" % (str(currhive.bestposition)))
                    print("Best fitness: %f" % currhive.bestfitness)

                    # if n % 10 == 0:
                    #     beePlotting.plotswarm(currhive, 2, 3)



                # Сохраним значения целевой функции
                # fname = stat_fname % (("%4.4d" % runnumber) + "_fitness")
                # fp = file(fname, "w")
                # fp.write(stat.formatfitness(runnumber))
                # fp.close()
                #
                # # Сохраним значения координат
                # fname = stat_fname % (("%4.4d" % runnumber) + "_pos")
                # fp = file(fname, "w")
                # fp.write(stat.formatpos(runnumber))
                # fp.close()
                #
                # # Сохраним значения интервалов
                # fname = stat_fname % (("%4.4d" % runnumber) + "_range")
                # fp = file(fname, "w")
                # fp.write(stat.formatrange(runnumber))
                # fp.close()

            # Отображение статистики
            # beePlotting.plotstat(stat)

    window.close()