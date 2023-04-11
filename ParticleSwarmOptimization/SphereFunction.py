from Swarm import Swarm

class Swarm_Sphere (Swarm):
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
        penalty = self._getPenalty (position, 10000.0)
        finalfunc = sum (position * position)

        return finalfunc + penalty

    def function_for_plot(self, positionX, positionY):
        return positionX * positionX + positionY * positionY