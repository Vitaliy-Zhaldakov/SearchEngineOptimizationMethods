from RastriginFunction import Swarm_Rastrigin
from SchwefelFunction import Swarm_Schwefel
from SphereFunction import Swarm_Sphere
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PySimpleGUI as gui
import numpy as np

if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Оптимизация роя частиц", justification='center', size=(50, 1), font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Размерность выборки:", font=('ComicSans', 12)), gui.InputText(2, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Число итераций:", font=('ComicSans', 12), size=(19,1)), gui.InputText(500, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Размер популяции:", font=('ComicSans', 12), size=(19,1)), gui.InputText(300, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Нижняя граница:", font=('ComicSans', 12), size=(19,1)), gui.InputText(-5, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Верхняя граница:", font=('ComicSans', 12), size=(19,1)), gui.InputText(5, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Общий коэффициент для скорости:", font=('ComicSans', 12)), gui.InputText(0.5, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Коэффициент влияния лучшей точки каждой частицы на будущую скорость:", font=('ComicSans', 12)), gui.InputText(2.0, font=('ComicSans', 12), size=(10,1))],
        [gui.Text("Коэффициент влияния лучшей глобальной точки частиц на будущую скорость:", font=('ComicSans', 12)), gui.InputText(5.0, font=('ComicSans', 12), size=(10,1))],
        [gui.Radio("Функция Растригина", "Radio1", default=True, key="Rastrigin", font=('ComicSans', 12)),
         gui.Radio("Функция Швефеля", "Radio1", default=False, key="Schwefel", font=('ComicSans', 12)),
         gui.Radio("Функция Сферы", "Radio1", default=False, key="Sphere", font=('ComicSans', 12))],
        [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Оптимизация роя частиц', layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            # Размерность выборки
            dimension = int(values[0])
            # Число итераций
            iterCount = int(values[1])
            # Размер популяции
            swarmsize = int(values[2])
            # Границы выборки
            minvalues = np.array([float(values[3])] * dimension)
            maxvalues = np.array([float(values[4])] * dimension)
            # Общий коэффициент для скорости (k)
            currentVelocityRatio = float(values[5])
            # Коэффициент влияния лучшей точки каждой частицы на будущую скорость (phi(p))
            localVelocityRatio = float(values[6])
            # Коэффициент влияния лучшей глобальной точки частиц на будущую скорость (phi(g))
            globalVelocityRatio = float(values[7])

            if values["Rastrigin"] == True:
                # Рой для функции Растригина
                swarm = Swarm_Rastrigin(swarmsize,
                                        minvalues,
                                        maxvalues,
                                        currentVelocityRatio,
                                        localVelocityRatio,
                                        globalVelocityRatio)
            elif values["Schwefel"]:
                # Рой для функции Швефеля
                swarm = Swarm_Schwefel(swarmsize,
                                       minvalues,
                                       maxvalues,
                                       currentVelocityRatio,
                                       localVelocityRatio,
                                       globalVelocityRatio)
            else:
                # Рой для функции сферы
                swarm = Swarm_Sphere(swarmsize,
                                    minvalues,
                                    maxvalues,
                                    currentVelocityRatio,
                                    localVelocityRatio,
                                    globalVelocityRatio)

            # Построение графика
            x = np.arange(float(values[3]), float(values[4]), 0.1)
            y = np.arange(float(values[3]), float(values[4]), 0.1)
            x_plot, y_plot = np.meshgrid(x, y)
            fun_plot = swarm.function_for_plot(x_plot, y_plot)

            # 3D График
            ax = plt.figure().add_subplot(111, projection='3d')
            ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

            for iter in range (iterCount):
                #print ("Position", swarm[0].position)
                #print ("Velocity", swarm[0].velocity)
                swarm.nextIteration()

            # Оптимум функции
            print(swarm.globalBestPosition, swarm.globalBestFinalFunc)
            # Отображение точки минимума
            ax.scatter(swarm.globalBestPosition[0], swarm.globalBestPosition[1], swarm.globalBestFinalFunc, color='red')
            plt.show()

    window.close()



