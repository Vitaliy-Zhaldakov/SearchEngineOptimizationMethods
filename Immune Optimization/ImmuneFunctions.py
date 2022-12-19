import numpy as np
from ImmuneNetwork import immuneNetwork

class rosenbrock(immuneNetwork):
    """Класс функции Розенброка"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        super().__init__(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

    def fitness_function(self, x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


class himmelblau(immuneNetwork):
    """Класс функции Химмельблау"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        super().__init__(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

    def fitness_function(self, x, y):
        return ((x ** 2 + y - 11) ** 2) + (x + y ** 2 - 7) ** 2


class rastrigin(immuneNetwork):
    """Класс функции Растригина"""

    def __init__(self, minValue, maxValue, size_Sb, nb, intensiveParam, iterations):
        super().__init__(minValue, maxValue, size_Sb, nb, intensiveParam, iterations)

    def fitness_function(self, x, y):
        return 20.0 + ((x * x - 10.0 * np.cos (2 * np.pi * x) +
                                               (y * y - 10.0 * np.cos (2 * np.pi * y))))