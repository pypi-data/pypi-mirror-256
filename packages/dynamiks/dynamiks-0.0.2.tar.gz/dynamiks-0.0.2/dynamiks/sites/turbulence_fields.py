import hipersim
from py_wake.utils.grid_interpolator import GridInterpolator
import xarray as xr
import numpy as np
from pathlib import Path
from numpy import newaxis as na


class RandomTurbulence():
    def __init__(self, ti, ws, seed=12345, uvw_scaling=[1, .8, .5]):
        self.sigma = ti * ws * np.array(uvw_scaling)
        self.rng = np.random.default_rng(seed)

    def initialize(self, flowSimulation):
        pass

    def __call__(self, x, *_, **__):
        if np.any(self.sigma > 0):
            return (self.rng.standard_normal((3,) + np.shape(x)).T * self.sigma).T
        else:
            return np.zeros((3,) + np.shape(x))


class MannTurbulenceField(hipersim.MannTurbulenceField):
    def __init__(self, offset, uvw, alphaepsilon, L, Gamma, Nxyz, dxyz, seed=None, HighFreqComp=0,
                 double_xyz=(False, True, True), n_cpu=1, random_generator=None, generator='unknown'):
        hipersim.MannTurbulenceField.__init__(self, uvw, alphaepsilon, L, Gamma, Nxyz, dxyz, seed=seed,
                                              HighFreqComp=HighFreqComp, double_xyz=double_xyz, n_cpu=n_cpu,
                                              random_generator=random_generator, generator=generator)

        self.offset = np.array(offset, dtype=float)
        self.x, self.y, self.z = [np.arange(N) * d for N, d in zip(self.Nxyz, self.dxyz)]

    def initialize(self, flowSimulation):
        self.transport_speed = flowSimulation.site.ws

    @staticmethod
    def from_netcdf(filename, offset):
        da = xr.load_dataarray(filename)
        return MannTurbulenceField.from_xarray(da, offset)

    @staticmethod
    def from_xarray(dataArray, offset):
        da = dataArray
        return MannTurbulenceField(offset, da.values,
                                   Nxyz=da.shape[1:],
                                   dxyz=[(v[1] - v[0]).item() for v in (da.x, da.y, da.z)],
                                   generator=da.attrs['Generator'],
                                   **{k: da.attrs[k] for k in da.attrs if k not in ['Generator', 'name']}
                                   )

    @staticmethod
    def from_hawc2(filenames, offset, Nxyz, dxyz,
                   alphaepsilon, L, Gamma,  # used for scaling
                   seed=1, HighFreqComp=False, double_xyz=(False, True, True)  # only used to generate name
                   ):
        uvw = np.reshape([np.fromfile(f, np.dtype('<f'), -1) for f in filenames], (3,) + tuple(Nxyz))
        return MannTurbulenceField(offset, uvw, alphaepsilon, L, Gamma, Nxyz, dxyz,
                                   seed, HighFreqComp, double_xyz)

    @staticmethod
    def generate(offset, alphaepsilon=1, L=33.6, Gamma=3.9, Nxyz=(8192, 64, 64),
                 dxyz=(1, 1, 1), seed=1, HighFreqComp=0, double_xyz=(False, False, False),
                 n_cpu=1, verbose=0, random_generator=None, cache_spectral_tensor=False):
        mtf = hipersim.MannTurbulenceField.generate(alphaepsilon=alphaepsilon, L=L, Gamma=Gamma,
                                                    Nxyz=Nxyz, dxyz=dxyz, seed=seed, HighFreqComp=HighFreqComp,
                                                    double_xyz=double_xyz, n_cpu=n_cpu, verbose=verbose,
                                                    random_generator=random_generator,
                                                    cache_spectral_tensor=cache_spectral_tensor)
        return MannTurbulenceField.from_xarray(mtf.to_xarray(), offset)

    def get_axes(self, time):
        offset = self.offset.copy()
        if time > 0:
            offset[0] += self.transport_speed * time
        return [xyz + o for xyz, o in zip([self.x, self.y, self.z], offset)]

    def get_slice(self, values, axis, time):
        values = np.atleast_1d(values)
        ax = self.get_axes(time)[axis]
        x0 = ax[0]
        dx = ax[1] - x0
        xi = int(np.floor((values.min() - x0) / dx))
        Nx = int((values.max() - values.min()) // dx) + 1
        N = len(ax)
        if xi < 0 or xi + Nx > N:
            # repeat box
            assert self.double_xyz[axis] == 0, "Not implement for mirrored axes"
            return np.arange(xi, xi + Nx + 1)  # % N
        else:
            return slice(xi, xi + Nx + 1)

    def __call__(self, x, y, z, time):
        x = x - self.offset[0]
        if time != 0:
            x -= self.transport_speed * time
        y = y - self.offset[1]
        z = z - self.offset[2]
        return np.moveaxis(hipersim.MannTurbulenceField.__call__(self, x, y, z), -1, 0).astype(float)
