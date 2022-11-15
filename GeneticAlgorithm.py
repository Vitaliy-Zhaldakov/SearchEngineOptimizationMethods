import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def function(x,y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

# Инициализация исходной популяции
def create_population(num_individuals, x_min, x_max):
    population = []
    for i in range(num_individuals):
        population.append([random.uniform(x_min, x_max), random.uniform(x_min, x_max)])
    return population

# Метод панмиксии для отбора пар родителей
def panmixia(population):
    pairsOfParents = []
    num_individuals = len(population)
    for i in range(num_individuals):
        randomParent = random.randint(0, num_individuals-1)
        pairsOfParents.append([population[i], population[randomParent]])
    return pairsOfParents

# Метод линейной рекомбинации
def linear_recombination(pairsOfParents):
    newPopulation = []
    for i in range(len(pairsOfParents)):
        alpha = random.uniform(-0.25, 1.25)
        firstParent = pairsOfParents[i][0]
        secondParent = pairsOfParents[i][1]
        newPopulation.append([firstParent[0] + alpha * (secondParent[0] - firstParent[0]), firstParent[1] + alpha * (secondParent[1] - firstParent[1])])
    return newPopulation

# Метод турнирного отбора
def tournament_selection(num_individuals, population):
    newPopulation = []
    t = int(num_individuals / 4)
    for i in range(num_individuals):
        intermediateArray = []
        for j in range(t):
            num = random.randint(0, num_individuals - 1)
            intermediateArray.append([function(population[num][0], population[num][1]), population[num][0], population[num][1]])
        intermediateArray.sort()
        newPopulation.append([intermediateArray[0][1], intermediateArray[0][2]])
    return newPopulation

# Метод элитарного отбора
def elite_selection(num_individuals,population):
    newPopulation = []
    for elem in population:
        newPopulation.append([function(elem[0], elem[1]), elem[0], elem[1]])
    newPopulation.sort()
    resultSelection = []

    # Отбор 10% элитных особей
    elite = int(num_individuals * 0.1)
    for i in range(elite):
        resultSelection.append([newPopulation[elite][1],newPopulation[elite][2]])
    restIndividuals = truncation_selection(num_individuals-elite, population[elite:])
    resultSelection += restIndividuals
    return resultSelection

# Метод отбора усечением
def truncation_selection(num_individuals, population):
    newPopulation = []
    for elem in population:
        newPopulation.append([function(elem[0],elem[1]), elem[0], elem[1]])
    newPopulation.sort()
    resultSelection = []
    for i in range(num_individuals):
        percent = random.uniform(0,1)
        individ = random.randint(0,int(len(newPopulation) * percent))
        resultSelection.append([newPopulation[individ][1],newPopulation[individ][2]])
    return resultSelection

# Вещественная мутация
def mutation(population, chance, step):
    for i in range(len(population)):
        for j in range(2):
            randomValue = random.uniform(0,1)

            if randomValue < chance:
                population[i][j]+= step if randomValue < chance/2 else -step
    return population

# Генетический алгоритм
def genetic_algorithm(num_individuals, min_x, max_x, numGenerations, mutationChance, mutationStep):
    population = create_population(num_individuals, min_x, max_x)
    for generation in range(numGenerations):
        pairsOfParents = panmixia(population)

        children = linear_recombination(pairsOfParents)
        children = mutation(children, mutationChance, mutationStep)

        population += children
        population = elite_selection(num_individuals, population)

    # Выбор самой приспособленной особи
    bestFunction = function(population[0][0], population[0][1])
    bestIndivid = population[0]
    for individ in population:
        if function(individ[0], individ[1]) < bestFunction:
            bestIndivid = individ
            bestFunction = function(individ[0], individ[1])
    return [bestIndivid, bestFunction]

def main():
    result = genetic_algorithm(100, -5, 5, 100, 0.01, 0.1)
    print("Хромосома лучшей особи: ", result[0])
    print("Значение приспособленности: ", result[1])

    # Построение графика
    x_p = np.arange(-5, 5, 0.1)
    y_p = np.arange(-5, 5, 0.1)
    x_plot, y_plot = np.meshgrid(x_p, y_p)
    fun_plot = function(x_plot, y_plot)

    # 3D График
    ax = plt.figure().add_subplot(111, projection='3d')
    # Отображение точки минимума
    ax.scatter(result[0][0], result[0][1], result[1], color='red')
    ax.plot_surface(x_plot, y_plot, fun_plot, rstride=5, cstride=5, alpha=0.7)

    plt.show()

if __name__ == "__main__":
    main()