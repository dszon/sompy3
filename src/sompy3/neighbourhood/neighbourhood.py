import numpy as np
import inspect
import sys

EPS = 0.000000000000001

class compNeighbourhood(object):

    @staticmethod
    # ========================================================================================================================================
    def init(neighborhoodMethod,mapsize):
    # ========================================================================================================================================
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if hasattr(obj, 'name') and neighborhoodMethod == obj.name:
                    o = obj(mapsize)
                    return o
        else:
            raise NotImplementedError("Unknown neighbourhood type {:s} (not implemented)".format(neighborhoodMethod))

# ========================================================================================================================================
class GaussianNeighborhood(object):
# ========================================================================================================================================

    name = 'gaussian'

    # ----------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,mapsize):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        self.neighbourhoodField = self._calculateField(mapsize)
        self.mapsize            = mapsize

    # ----------------------------------------------------------------------------------------------------------------------------------------
    def calculate(self, radius, node):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        xs = self.mapsize[0]   - node[0]
        xe = 2*self.mapsize[0] - node[0]
        ys = self.mapsize[1]   - node[1]
        ye = 2*self.mapsize[1] - node[1]
        d = self.neighbourhoodField[xs:xe,ys:ye]
        return np.exp(-1.0*d/(2*radius**2))

    @staticmethod
    # ----------------------------------------------------------------------------------------------------------------------------------------
    def _calculateField(mapsize):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        d = np.zeros([3*mapsize[0],3*mapsize[1]])
        for i in range(3*mapsize[0]):
            for j in range(3*mapsize[1]):
                d[i,j] = (i-mapsize[0])**2 + (j-mapsize[1])**2
        return d

    # ----------------------------------------------------------------------------------------------------------------------------------------
    def __call__(self, *args, **kwargs):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        return self.calculate(*args)





# ========================================================================================================================================
class BubbleNeighborhood(object):
# ========================================================================================================================================

    name = 'blob'

    # ----------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,mapsize):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        self.neighbourhoodField = self._calculateField(mapsize)
        self.mapsize            = mapsize

    # ----------------------------------------------------------------------------------------------------------------------------------------
    def calculate(self, radius, node):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        xs = self.mapsize[0]   - node[0]
        xe = 2*self.mapsize[0] - node[0]
        ys = self.mapsize[1]   - node[1]
        ye = 2*self.mapsize[1] - node[1]
        d  = self.neighbourhoodField[xs:xe,ys:ye]
        z  = np.zeros(d.shape)
        mx = radius**2
        z[d <= mx] = 1 #/(100*radius**2)
        return z

    @staticmethod
    # ----------------------------------------------------------------------------------------------------------------------------------------
    def _calculateField(mapsize):
    # ----------------------------------------------------------------------------------------------------------------------------------------
        d = np.zeros([3*mapsize[0],3*mapsize[1]])
        for i in range(3*mapsize[0]):
            for j in range(3*mapsize[1]):
                d[i,j] = (i-mapsize[0])**2 + (j-mapsize[1])**2
        return d

    def __call__(self, *args, **kwargs):
        return self.calculate(*args)