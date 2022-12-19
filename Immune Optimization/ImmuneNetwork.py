import random
import math

class immuneNetwork:
    """Класс иммунной сети"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        self.minValue = minValue
        self.maxValue = maxValue
        self.size_Sb = size_Sb
        self.nb = nb
        self.intensiveParam = intensiveParam
        self.iterations = iterations

    def fitness_function(self):
        pass

    def generate_population(self, minValue, maxValue, num):
        """Генерация начальной популяции"""
        population = []
        for i in range(num):
            population.append([random.uniform(minValue, maxValue), random.uniform(minValue, maxValue)])
        return population

    def get_best_antibodies(self, antibodies, nb):
        """Получаем лучшие антитела"""
        sub_antibodies = antibodies.copy()
        sub_antibodies.sort(key=lambda x: self.fitness_function(x[0], x[1]), reverse=False)
        sub_antibodies = sub_antibodies[:nb]
        return sub_antibodies

    def cloning_and_mutation(self, antibodies, intensiveParam):
        """Клонирование и мутация лучших антител"""
        clones = []
        for body in antibodies:
            alpha = math.exp(-intensiveParam * self.fitness_function(body[0], body[1]))
            clones.append([body[0] + alpha * random.uniform(-0.5, 0.5), body[1] + alpha * random.uniform(-0.5, 0.5)])
        return clones

    def generate_new_population(self, Sm, clones, nb, minValue, maxValue):
        """Создание новой популяции антител"""
        newPopulation = []
        for i in range(len(Sm)):
            if (self.fitness_function(clones[i][0], clones[i][1]) < self.fitness_function(Sm[i][0], Sm[i][1])):
                newPopulation.append(clones[i])
            else:
                newPopulation.append(Sm[i])

        newPopulation += self.generate_population(minValue, maxValue, nb)
        return newPopulation