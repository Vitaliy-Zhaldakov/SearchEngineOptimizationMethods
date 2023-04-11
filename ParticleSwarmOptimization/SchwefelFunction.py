import numpy as np
from Swarm import Swarm

class Swarm_Schwefel (Swarm):
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


    def _finalFunc (self, position):
        function = sum (-position * np.sin (np.sqrt (np.abs (position) ) ) )
        penalty = self._getPenalty (position, 10000.0)
        return function + penalty

    def function_for_plot(self, positionX, positionY):
        return (-positionX * np.sin(np.sqrt(np.abs(positionX)))) + (-positionY * np.sin(np.sqrt(np.abs(positionY))))
