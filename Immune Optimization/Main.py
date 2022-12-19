import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import PySimpleGUI as gui
from ImmuneFunctions import rosenbrock
from ImmuneFunctions import himmelblau
from ImmuneFunctions import rastrigin
import time

if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Алгоритм иммунной сети", justification='center', size=(50, 1), font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Минимальное значение:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(-6, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Максимальное значение:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(6, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Размер начальной популяции антител:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(100, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число антител для клонирования:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(40, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Параметр интенсивности:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(0.3, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Количество итераций:", font=('ComicSans', 12), size=(31, 1)),
         gui.InputText(100, font=('ComicSans', 12), size=(10, 1))],
        [gui.Radio("Функция Розенброка", "Radio1", default=True, key="Rosenbrock", font=('ComicSans', 12)),
         gui.Radio("Функция Химмельблау", "Radio1", default=False, key="Himmelblau", font=('ComicSans', 12)),
         gui.Radio("Функция Растригина", "Radio1", default=False, key="Rastrigin", font=('ComicSans', 12))],
        [gui.T("   ")],
        [gui.Text(key='result', font=('ComicSans', 12))],
        [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Алгоритм иммунной сети', layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            # Минимальное значение
            minValue = int(values[0])
            # Максимальное значение
            maxValue = int(values[1])
            # Размер начальной популяции антител
            size_Sb = int(values[2])
            # Число антител для мутации
            nb = int(values[3])
            # Параметр интенсивности
            intensiveParam = float(values[4])
            # Количество итераций
            iterations = int(values[5])

            if values["Rosenbrock"] == True:
                network = rosenbrock(minValue, maxValue, size_Sb, nb, intensiveParam,iterations)
            elif values["Himmelblau"]:
                network = himmelblau(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)
            else:
                network = rastrigin(minValue, maxValue, size_Sb, nb, intensiveParam,iterations)

            time1 = time.time()
            time_list = []
            solution = []

            # Генерация случайной популяции
            Sb = network.generate_population(minValue, maxValue, size_Sb)
            for i in range(iterations):
                # Получение лучших антител
                Sm = network.get_best_antibodies(Sb, nb)
                # Получение мутантных клонов
                clones = network.cloning_and_mutation(Sm, intensiveParam)
                # Создание новой популяции с учетом клонов
                Sb = network.generate_new_population(Sm, clones, nb, minValue, maxValue)

                # Нахождение лучшего решения в популяции
                best_solution = network.fitness_function(Sb[0][0], Sb[0][1])
                best_index = 0
                for i in range(1, len(Sb)):
                    if network.fitness_function(Sb[i][0], Sb[i][1]) < best_solution:
                        best_index = i
                        best_solution = network.fitness_function(Sb[i][0], Sb[i][1])
                result = [Sb[best_index], best_solution]

                # Точки времени
                time_list.append(time.time() - time1)
                # Точки решений
                solution.append(result[1])

            # Вывод результата
            window['result'].update(f"Результат: {result}")

            # Построение графика эффективности
            fig, ax = plt.subplots()
            ax.plot(time_list, solution)
            plt.title("График эффективности алгоритма")
            plt.xlabel("Время")
            plt.ylabel("Значение лучшего решения")
            plt.show()

            # Построение 3D графика
            x = np.arange(float(values[0]), float(values[1]), 0.1)
            y = np.arange(float(values[0]), float(values[1]), 0.1)
            x_plot, y_plot = np.meshgrid(x, y)
            fun_plot = network.fitness_function(x_plot, y_plot)

            # 3D График
            ax = plt.figure().add_subplot(111, projection='3d')
            ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

            # Отображение точки минимума
            ax.scatter(result[0][0], result[0][1], result[1], color='red')
            plt.show()

    window.close()