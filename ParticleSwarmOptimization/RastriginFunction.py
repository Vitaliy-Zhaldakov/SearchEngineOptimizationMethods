import numpy as np
from Swarm import Swarm

# Рой функции Растригина
class Swarm_Rastrigin (Swarm):
    def __init__ (self,
            swarmsize,
            minvalues,
            maxvalues,
            currentVelocityRatio,
            localVelocityRatio,
            globalVelocityRatio):
       Swarm.__init__ (self,
            swarmsize,
            minvalues,
            maxvalues,
            currentVelocityRatio,
            localVelocityRatio,
            globalVelocityRatio)

    # Переопределение метода вычисления функции
    def _finalFunc (self, position):
        function = 10.0 * len (self.minvalues) + sum (position * position - 10.0 * np.cos (2 * np.pi * position))
        # Штраф частицы
        penalty = self._getPenalty (position, 10000.0)
        return function + penalty

    def function_for_plot(self, positionX, positionY):
        return 10.0 * len (self.minvalues) + ((positionX * positionX - 10.0 * np.cos (2 * np.pi * positionX) +
                                               (positionY * positionY - 10.0 * np.cos (2 * np.pi * positionY))))

    def function(self, position):
        return 10.0 * len (self.minvalues) + (position * position - 10.0 * np.cos (2 * np.pi * position))