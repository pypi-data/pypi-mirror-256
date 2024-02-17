import inspect

import matplotlib.pyplot as plt
import numpy as np
from py_wake.wind_turbines._wind_turbines import WindTurbines as WindTurbinesPW
from py_wake.deficit_models.utils import ct2a_madsen
from dynamiks.wind_turbines.axisymetric_induction import InductionMatch

from dynamiks.wind_turbines._windTurbines import WindTurbines
from numpy import newaxis as na
from multiclass_interface.multiprocess_interface import MultiProcessClassInterface
import atexit


class PyWakeWindTurbines(WindTurbines):
    def __init__(self, x, y, windTurbine, types=0, z=0, inductionModel=None):
        assert len(x) == len(y)
        WindTurbines.__init__(self, windTurbine._names, N=len(x))
        assert isinstance(windTurbine, WindTurbinesPW)
        z = np.zeros_like(x) + z
        self.position = np.array([x, y, z])
        self.rotor_position = np.array([x, y, z + windTurbine.hub_height(types)])

        self.inductionModel = inductionModel or InductionMatch()
        self.windTurbine = windTurbine
        self.types = np.zeros(len(x), dtype=int) + types
        self._yaw = np.zeros(len(x))
        self._tilt = np.zeros(len(x))

    @property
    def yaw(self):
        return self._yaw

    @yaw.setter
    def yaw(self, yaw):
        self._yaw[:] = yaw

    @property
    def tilt(self):
        return self._tilt

    @tilt.setter
    def tilt(self, tilt):
        self._tilt[:] = tilt

    def __getitem__(self, idx):
        class WindTurbine():
            def __init__(self, windTurbines, idx):
                self.windTurbines = windTurbines
                self.idx = idx

            @property
            def rotor_position(self):
                return self.windTurbines.rotor_position[:, idx]

            def __getattr__(self, name):
                attr = getattr(self.windTurbines, name)
                if inspect.ismethod(attr) and 'idx' in inspect.getfullargspec(attr).args:
                    def wrap(*args, **kwargs):
                        res = getattr(self.windTurbines, name)(*args, idx=self.idx, **kwargs)
                        if isinstance(self.idx, int):
                            res = res[..., na]
                        return res
                    return wrap
                else:
                    return attr
        return WindTurbine(self, idx)

    def diameter(self, idx=slice(None)):
        return self.windTurbine.diameter(self.types[idx])

    def hub_height(self, idx=slice(None)):
        return self.windTurbine.hub_height(self.types[idx])

    def ct(self, ws=None, idx=slice(None)):
        options = {'type': self.types[idx]}
        kwargs = {k: options[k] for k in self.windTurbine.powerCtFunction.required_inputs}
        if ws is None:
            ws = self.rotor_avg_windspeed(include_wakes=True, idx=idx)[0]
        return self.windTurbine.ct(ws, **kwargs)

    def power(self, include_wakes=True, idx=slice(None)):
        options = {'type': self.types[idx]}
        kwargs = {k: options[k] for k in self.windTurbine.powerCtFunction.required_inputs}

        return self.windTurbine.power(self.rotor_avg_windspeed(idx=idx, include_wakes=include_wakes)[0], **kwargs)

    def rotor_avg_induction(self, idx=slice(None)):
        return ct2a_madsen(self.ct(idx=idx))

    def axisymetric_induction(self, r, idx=slice(None)):
        tsr = 7
        a_target_lst = self.rotor_avg_induction(idx)
        a = np.moveaxis([self.inductionModel(tsr=tsr, a_target=a_target, r=r)[1]
                         for a_target in np.atleast_1d(a_target_lst)], 0, -1)
        if isinstance(idx, int):
            a = a[..., 0]
        return a

    def yaw_tilt(self, idx=slice(None)):
        return np.array([self.yaw[idx], self.tilt[idx]])


class DummyWT():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ParallelPyWakeWindTurbines(PyWakeWindTurbines):
    def __init__(self, x, y, windTurbine, types=0, z=0, inductionModel=None):
        PyWakeWindTurbines.__init__(self, x, y, windTurbine, types=types, z=z, inductionModel=inductionModel)
        self.dist_wt = MultiProcessClassInterface(DummyWT, [(x, y) for x, y in zip(x, y)])
        atexit.register(self.dist_wt.close)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dist_wt.close()
