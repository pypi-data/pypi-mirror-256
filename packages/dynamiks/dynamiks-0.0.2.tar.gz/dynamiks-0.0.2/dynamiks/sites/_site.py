from abc import ABC
import numpy as np
from numpy import newaxis as na
from dynamiks.views import Grid3D, Points, Grid, View
from py_wake.site.shear import Shear as PyWakeShear


class Site(ABC):
    ""


class TurbulenceFieldSite(Site):
    def __init__(self, ws, ti, turbulenceField, shear=None):
        self.ws = ws
        self.ti = ti
        self.turbulenceField = turbulenceField
        assert isinstance(shear, PyWakeShear) or shear is None, "Shear must be PyWake shear or None"
        self.shear = shear
        self.time = 0
        self.step_handlers = [self.step]

    def initialize(self, flowSimulation):
        self.turbulenceField.initialize(flowSimulation)

    def add_mean_wind(self, xyz, uvw):
        U = self.ws
        if isinstance(self.shear, PyWakeShear):
            class LocalWind():
                coords = {}
            U = self.shear(localWind=LocalWind(), WS_ilk=U, h=np.maximum(xyz[2], 0))[:, 0, 0]
        uvw[0] += U
        return uvw

    def get_windspeed(self, view, time=None):
        if time is None:
            time = self.time
        assert isinstance(view, View)
        if isinstance(view, Points):
            xyz = view.XYZ
            uvw = self.turbulenceField(*xyz, time)
        elif (isinstance(view, Grid3D) or view.adaptive) and hasattr(self.turbulenceField, 'get_axes'):
            def slice_repeat(s, N):
                if isinstance(s, np.ndarray):
                    s = np.atleast_1d(s % N)
                return s

            if isinstance(view, Grid3D):
                slices = view.slices
            else:
                slices = view.get_slices(*self.turbulenceField.get_axes(time))
            shape = self.turbulenceField.uvw.shape[1:]
            x_slice, y_slice, z_slice = [slice_repeat(s, N) for s, N in zip(slices, shape)]
            xyz = view.XYZ
            s = (3,) + view.shape
            uvw = self.turbulenceField.uvw[:, x_slice][:, :, y_slice][:, :, :, z_slice].reshape(s).copy(order='F')
            uvw = uvw.astype(float)
        elif isinstance(view, Grid):
            if any([v is None for v in view]):
                adap_err = ["", "or set adaptive to True "][hasattr(self.turbulenceField, 'x')]
                err = f'Grid undefined. Please specify the grid explicitly {adap_err}when instantiating {view.__class__.__name__}'
                raise TypeError(err)
            xyz = view.XYZ
            uvw = self.turbulenceField(*xyz, time=time)

        else:  # pragma: no cover
            raise NotImplementedError(xyz.__class)
        return self.add_mean_wind(xyz, uvw)

    def get_turbulence_intensity(self, xyz):
        return self.get_windspeed(xyz)[0] * 0 + self.ti

    def step(self, flowSimulation):
        self.time = flowSimulation.time
