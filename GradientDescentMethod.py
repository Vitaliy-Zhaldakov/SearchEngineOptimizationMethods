# Метод градиентного спуска с постоянным шагом
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PySimpleGUI as gui

# Исходная функция
def function(x):
    return 2 * pow(x[0], 2) + x[0] * x[1] + pow(x[0], 2)

# Другой вид исходной функции
def plot_function(x, y):
    return 2 * pow(x, 2) + x * y + pow(x, 2)

# Частная производная по х1
def diff_x(x):
    return 4 * x[0] + x[1]

# Частная производная по х2
def diff_y(x):
    return x[0] + 2 * x[1]

# Градиент функции
def grad(x):
    return [diff_x(x), diff_y(x)]

# Вычисление следующей координаты точки
def next_x(x, t):
    temp = grad(x)
    return x[0] - t*temp[0], x[1] - t*temp[1]

# Функция нормирования вектора
def norm(vector):
    res = 0
    for i in vector:
        res += i**2
    return math.sqrt(res)

def main():
    gui.theme_background_color('#f2e8c9')
    gui.theme_text_element_background_color('#f2e8c9')
    gui.theme_button_color('#9D8741')
    gui.theme_text_color('Black')

    layout = [
        [gui.Text("Метод градиентного спуска", justification='center', size=(50, 1), font=('ComicSans', 16))],
        [gui.Text("X = ", font=('ComicSans', 12)), gui.InputText(0.5, font=('ComicSans', 12))],
        [gui.Text("Y = ", font=('ComicSans', 12)), gui.InputText(1, font=('ComicSans', 12))],
        [gui.Text("eps = ", font=('ComicSans', 12)), gui.InputText(0.01, font=('ComicSans', 12))],
        [gui.Text("eps1 = ", font=('ComicSans', 12)), gui.InputText(0.005, font=('ComicSans', 12))],
        [gui.Text("eps2 = ", font=('ComicSans', 12)), gui.InputText(0.005, font=('ComicSans', 12))],
        [gui.Text("M = ", font=('ComicSans', 12)), gui.InputText(20, font=('ComicSans', 12))],
        [gui.Text("t = ", font=('ComicSans', 12)), gui.InputText(0.01, font=('ComicSans', 12))],
        [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Градиентный спуск', layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            x = [float(values[0]), float(values[1])]
            eps = float(values[2])
            eps1 = float(values[3])
            eps2 = float(values[4])
            m = float(values[5]) # Предельное число итераций
            t = float(values[6]) # Шаг алгоритма

            k = 0

            resolved = False
            while k <= m and not resolved:
                k += 1
                if eps1 > norm(grad(x)):
                    resolved = True
                else:
                    newx, newy = next_x(x, t)
                    while not (function([newx, newy]) - function(x) < 0 or math.fabs(function([newx, newy]) - function(x)) < eps * norm(grad(x)) ** 2):
                        x[0], x[1] = newx, newy
                        newx, newy = next_x(x, t)
                    if math.sqrt((x[0] - newx) ** 2 + (x[1] - newy) ** 2) < eps2 and math.fabs(function([newx, newy]) - function(x)) < eps2:
                        resolved = True
                    x[0], x[1] = newx, newy
                    print(x[0], x[1], function(x))

            print("Число итераций: " + k)
            # Построение графика
            x_p = np.arange(-5, 5, 0.1)
            y_p = np.arange(-5, 5, 0.1)
            x_plot, y_plot = np.meshgrid(x_p, y_p)
            fun_plot = plot_function(x_plot, y_plot)

            # 3D График
            ax = plt.figure().add_subplot(111, projection='3d')
            # Отображение точки минимума
            ax.scatter(x[0], x[1], plot_function(x[0], x[1]), color='red')
            ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)
            plt.show()

    window.close()


if __name__== "__main__":
    main()

