import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PySimpleGUI as gui


def sphereFunction(x, y):
    """Обратная функция сферы"""
    return -(x ** 2 + y ** 2)

def e_norma(x):
    """Евклидова норма"""
    return math.sqrt(x[0] ** 2 + x[1] ** 2)

def generate_population(populationSize, minValue, maxValue):
    """Инициализация популяции"""
    population = []
    for i in range(populationSize):
        bacteria = [[random.uniform(minValue, maxValue), random.uniform(minValue, maxValue)]]
        # Направляющий вектор бактерии (V)
        bacteria.append([random.uniform(-1, 1), random.uniform(-1, 1)])
        bacteria.append(sphereFunction(bacteria[0][0], bacteria[0][1]))
        population.append(bacteria.copy())
    return population


def chemotaxis(bacteria, chemotaxisStep):
    """Бактериальный хемотаксис"""
    operation = random.randint(0, 1)
    if operation == 0:
        # то движемся
        bacteria[0][0] = bacteria[0][0] + chemotaxisStep * bacteria[1][0] / (e_norma(bacteria[1]))
        bacteria[0][0] = bacteria[0][1] + chemotaxisStep * bacteria[1][1] / (e_norma(bacteria[1]))
    else:
        v = [random.uniform(-1, 1), random.uniform(-1, 1)]
        bacteria[0][0] = bacteria[0][0] + chemotaxisStep * v[0] / e_norma(v)
        bacteria[0][1] = bacteria[0][1] + chemotaxisStep * v[1] / e_norma(v)
        bacteria[1] = v
    bacteria[2] += sphereFunction(bacteria[0][0], bacteria[0][1])
    return bacteria

def reproduction(population):
    """Репродукция популяции"""
    count = len(population)
    population.sort(key=lambda a: a[2], reverse=True)
    population = population[:int(count / 2)]
    population += population.copy()
    return population

def elimination(population, eliminationNum, minValue, maxValue):
    """Ликвидация и рассеивание"""
    for i in range(eliminationNum):
        x = random.randint(0, (len(population) - 1))
        del population[x]
        new_bacteria = generate_population(1, minValue, maxValue)
        population += new_bacteria.copy()
    return population


def get_best_solution(population):
    """Нахождение лучшего решения текущей популяции"""
    best_solution = [population[0][0].copy()]
    best_solution.append(sphereFunction(best_solution[0][0], best_solution[0][1]))
    for bacteria in population:
        # print(bac)
        if sphereFunction(bacteria[0][0], bacteria[0][1]) > best_solution[1]:
            best_solution[0] = bacteria[0].copy()
            best_solution[1] = sphereFunction(bacteria[0][0], bacteria[0][1])
    return best_solution

def bacteria_algorithm(minValue, maxValue, populationSize, iterations, chemotaxisStep, eliminationNum, epsilon):
    """Бактериальный алгоритм"""

    if (populationSize % 2 != 0):
        print("Ошибка размерности популяции")
    else:
        population = generate_population(populationSize, minValue, maxValue)
        best = get_best_solution(population)

        global_best = best.copy()
        bestCurrent = best.copy()
        for i in range(iterations):
            # Плаваем, пока увеличивается значение фитнес-функции
            if bestCurrent[1] <= best[1]:
                best = bestCurrent.copy()
                for num in range(len(population)):
                    population[num] = chemotaxis(population[num], chemotaxisStep)
                bestCurrent = get_best_solution(population)
            # Иначе репродукция или ликвидация
            else:
                u = random.uniform(0, 1)
                if u > epsilon:
                    population = reproduction(population)
                else:
                    population = elimination(population, eliminationNum, minValue, maxValue)
                best = get_best_solution(population)
                bestCurrent = best.copy()

            if global_best[1] < bestCurrent[1]:
                global_best = bestCurrent.copy()
        global_best[1] = -global_best[1]
        return global_best


if __name__ == "__main__":
    gui.theme_background_color('White')
    gui.theme_text_element_background_color('White')
    gui.theme_button_color('Green')
    gui.theme_text_color('Black')
    gui.theme_element_background_color("White")

    layout = [
        [gui.Text("Алгоритм бактериальной оптимизации", justification='center', size=(40, 1), font=('ComicSans', 16))],
        [gui.T("   ")],
        [gui.Text("Минимальное значение:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(-5, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Максимальное значение:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(5, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Размер популяции:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(100, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Общее число итераций:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(200, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Величина шага хемотаксиса:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(0.1, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Число уничтожаемых особей:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(30, font=('ComicSans', 12), size=(10, 1))],
        [gui.Text("Вероятность ликвидации:", font=('ComicSans', 12), size=(24, 1)),
         gui.InputText(0.3, font=('ComicSans', 12), size=(10, 1))],
        [gui.T("   ")],
        [gui.Text(key='result', font=('ComicSans', 12))],
        [gui.Button('Вычислить', font=('ComicSans', 12))]]

    window = gui.Window('Алгоритм бактериальной оптимизации', layout)

    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break

        if event == 'Вычислить':
            minValue = int(values[0])
            maxValue = int(values[1])
            populationSize = int(values[2])
            iterations = int(values[3])
            stepChemotaxis = float(values[4])
            eliminationNum = int(values[5])
            epsilon = float(values[6])

            if (populationSize % 2 != 0):
                print("Ошибка размерности популяции")
                break

            # Построение графика
            x = np.arange(float(values[0]), float(values[1]), 0.1)
            y = np.arange(float(values[0]), float(values[1]), 0.1)
            x_plot, y_plot = np.meshgrid(x, y)
            fun_plot = sphereFunction(x_plot, y_plot)

            # 3D График
            ax = plt.figure().add_subplot(111, projection='3d')
            ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

            result = bacteria_algorithm(minValue, maxValue, populationSize, iterations, stepChemotaxis, eliminationNum, epsilon)
            window['result'].update(f"Результат: {result}")

            ax.scatter(result[0][0], result[0][1], result[1], color='red')
            plt.show()

    window.close()