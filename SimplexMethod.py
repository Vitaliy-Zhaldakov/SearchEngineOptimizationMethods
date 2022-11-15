from scipy.optimize import minimize, linprog
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_function(x, y):
    return 2 * pow(x,2) + 2 * x * y + 2 * pow(y,2) - 4 * x - 6 * y

def function(x):
    return 2 * pow(x[0],2) + 2 * x[0] * x[1] + 2 * pow(x[1],2) - 4 * x[0] - 6 * x[1]

# Ограничения функции
def constraint(x):
    x1 = x[0]
    x2 = x[1]
    return 2 - x1 - 2 * x2

def main():
    cons = ({'type': 'ineq', 'fun': constraint})
    bounds = ((0, None), (0, None))

    # Начальная точка
    x0 = np.array([2, 2])
    result = minimize(function, x0, method='SLSQP', constraints=cons, bounds=bounds)
    global_min = minimize(function, x0)

    x_first = x0
    x_min = result.x

    # Построение графика
    x_p = np.arange(-3, 3, 0.1)
    y_p = np.arange(-3, 3, 0.1)
    x_plot, y_plot = np.meshgrid(x_p, y_p)
    fun_plot = plot_function(x_plot, y_plot)

    # 3D График
    ax = plt.figure().add_subplot(111, projection='3d')
    # Отображение точки минимума
    ax.scatter(x_min[0], x_min[1], plot_function(x_min[0], x_min[1]), color='red')
    ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

    print("Исходные значения аргументов и функции:\n", x_first[0], x_first[1], function(x_first))
    print(f"Минимальные значения аргументов и функции:\n", x_min[0], x_min[1], function(x_min))
    # print(global_min.x[0], global_min.x[1], function(global_min.x))

    plt.show()

if __name__ == "__main__":
    main()
