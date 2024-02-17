import numpy as np
import matplotlib.pyplot as plt
from py_wake.wind_turbines import WindTurbines as WindTurbinesPW
from dynamiks.utils.geometry import get_east_north_height


class View():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, s):
        return [self.x, self.y, self.z][s]


class Points(View):
    def __init__(self, x, y, z):
        x, y, z = [np.atleast_1d(v) for v in [x, y, z]]
        assert len(x) == len(y) == len(z)
        View.__init__(self, x, y, z)

    # @property
    # def shape(self):
    #     return (len(self.x),)

    @property
    def XYZ(self):
        return self


class Grid(View):
    @property
    def shape(self):
        return np.shape(self.x) + np.shape(self.y) + np.shape(self.z)

    @property
    def XYZ(self):
        return np.reshape(np.meshgrid(self.x, self.y, self.z, indexing='ij'), (3,) + self.shape)


class Grid3D(Grid):
    def __init__(self, x_slice, y_slice, z_slice, axes):
        self.x_slice = x_slice
        self.y_slice = y_slice
        self.z_slice = z_slice
        self.slices = [x_slice, y_slice, z_slice]

        def get(ax, s):
            if isinstance(s, slice):
                return ax[s]
            else:
                x0, dx = ax[0], ax[1] - ax[0]
                assert np.allclose(np.diff(ax), dx), "axes must be equidistant"
                return s * dx + x0
        Grid.__init__(self, *[get(a, s) for a, s in zip(axes, [x_slice, y_slice, z_slice])])


class View2D(Grid):

    def __init__(self, x, y, z, adaptive, ax, xlim, ylim):
        if any([v is None for v in [x, y, z]]) and not adaptive:
            raise TypeError(
                f"Grid undefined. Please specify the grid explicitly when instantiating {self.__class__.__name__} or set adaptive to True")
        self.desired_x = x
        self.desired_y = y
        self.desired_z = z
        Grid.__init__(self, x, y, z)
        self.adaptive = adaptive
        self._ax = ax
        self.xlim = xlim or (getattr(self, self.plane[0]) is not None and getattr(self, self.plane[0])[[0, -1]])
        self.ylim = ylim or (getattr(self, self.plane[1]) is not None and getattr(self, self.plane[1])[[0, -1]])

    @property
    def ax(self):
        return self._ax or plt.gca()

    @ax.setter
    def ax(self, value):
        self._ax = value

    def XY(self, *_):
        return np.meshgrid(*[getattr(self, n) for n in self.plane])

    def get_slices(self, x, y, z):
        def get_slice(actual, xyz):
            dactual = actual[1] - actual[0]
            desired = getattr(self, f'desired_{xyz}')
            if desired is None:
                desired = actual
            ddesired = desired[1] - desired[0]
            actual[0]
            return np.arange(int(np.floor((desired.min() - actual[0]) / dactual)),
                             int(np.floor((desired.max() - actual[0]) / dactual) + 1),
                             np.maximum(int(np.floor(ddesired / dactual)), 1)
                             )

        slices = []
        for xyz, n in zip([x, y, z], 'xyz'):
            if n in self.plane:
                slices.append(get_slice(xyz, n))
            else:
                i = np.argmin(np.abs(xyz - getattr(self, n)))
                slices.append(np.array(i))

        self.x, self.y, self.z = [(x[1] - x[0]) * s + x[0] for x, s in zip([x, y, z], slices)]
        return slices

    def get_plot_windturbines(self):
        return lambda fs: self.plot_windturbines(fs)


class View1D(View2D):
    def __init__(self, x, y, z, adaptive, ax, xlim):
        x = self.desired_x = [np.asarray(x), None][x is None]
        y = self.desired_y = [np.asarray(y), None][y is None]
        z = self.desired_z = [np.asarray(z), None][z is None]
        Grid.__init__(self, x, y, z)
        self.adaptive = adaptive
        self._ax = ax
        self.xlim = xlim or (getattr(self, self.plane[0]) is not None and getattr(self, self.plane[0])[[0, -1]])

    @property
    def X(self):
        return getattr(self, self.plane)

    def plot_windturbines(self, fs, ax=None):
        ""


class XView(View1D):
    plane = 'x'

    def __init__(self, y, z, x=None, adaptive=True, ax=None, xlim=None):
        View1D.__init__(self, x, y, z, adaptive, ax, xlim)


class YView(View1D):
    plane = 'y'

    def __init__(self, x, z, y=None, adaptive=True, ax=None, ylim=None):
        View1D.__init__(self, x, y, z, adaptive, ax, ylim)


class ZView(View1D):
    plane = 'z'

    def __init__(self, x, y, z=None, adaptive=True, ax=None, zlim=None):
        View1D.__init__(self, x, y, z, adaptive, ax, zlim)


class XYView(View2D):
    plane = 'xy'

    def __init__(self, z, x=None, y=None, adaptive=True, ax=None, xlim=None, ylim=None):
        View2D.__init__(self, x, y, z, adaptive, ax, xlim, ylim)

    def plot_windturbines(self, fs):
        wt = fs.windTurbines
        x, y = wt.positions_xyz(fs.wind_direction, fs.center_offset)[:2]
        WindTurbinesPW.plot_xy(wt, x, y, types=wt.types, wd=270, ax=self.ax)


class EastNorthView(View2D):
    plane = 'xy'

    def __init__(self, h, east=None, north=None, adaptive=True, ax=None, east_lim=None, north_lim=None):
        View2D.__init__(self, east, north, h, adaptive, ax, east_lim, north_lim)

    def XY(self, wind_direction, center_offset):
        X, Y = np.meshgrid(*[getattr(self, n) for n in self.plane])
        return get_east_north_height([X, Y, X * 0], wind_direction, center_offset)[:2]

    def plot_windturbines(self, fs, ax=None):
        wt = fs.windTurbines
        x, y = wt.position[:2]
        WindTurbinesPW.plot_xy(wt, x, y, types=wt.types, wd=fs.wind_direction, ax=self.ax)


class XZView(View2D):
    plane = 'xz'

    def __init__(self, y, x=None, z=None, adaptive=True, ax=None, xlim=None, zlim=None):
        View2D.__init__(self, x, y, z, adaptive, ax, xlim, zlim)

    def plot_windturbines(self, fs):
        wt = fs.windTurbines
        x, z = wt.positions_xyz(fs.wind_direction, fs.center_offset)[[0, 2]]
        WindTurbinesPW.plot_yz(wt, x, z, types=wt.types, wd=180, ax=self.ax)


class YZView(View2D):
    plane = 'yz'

    def __init__(self, x, y=None, z=None, adaptive=True, ax=None, ylim=None, zlim=None):
        View2D.__init__(self, x, y, z, adaptive, ax, ylim, zlim)
        self.x = x

        self.adaptive = adaptive

    def plot_windturbines(self, fs):
        wt = fs.windTurbines
        y, z = wt.positions_xyz(fs.wind_direction, fs.center_offset)[[1, 2]]
        WindTurbinesPW.plot_yz(wt, y, z, types=wt.types, wd=270, ax=self.ax)
