import matplotlib.pyplot as plt
from py_wake.wind_turbines import WindTurbines as WindTurbinesPW
from abc import ABC, abstractmethod
import numpy as np
from dynamiks.utils.geometry import get_xyz


class WindTurbines(ABC):
    def __init__(self, names, N):
        self.N = N
        self.idx = np.arange(N)
        self._names = names
        self.step_handlers = []

    @abstractmethod
    def diameter(self, idx=slice(None)):
        ""

    @abstractmethod
    def hub_height(self, idx=slice(None)):
        ""

    def rotor_positions_xyz(self, wind_direction, center_offset):
        return get_xyz(self.rotor_position, wind_direction, center_offset)

    def positions_xyz(self, wind_direction, center_offset):
        return get_xyz(self.position, wind_direction, center_offset)

    def rotor_avg_windspeed(self, include_wakes, idx=slice(None)):
        if not isinstance(idx, (int, np.integer)):
            return np.array([WindTurbines.rotor_avg_windspeed(self, include_wakes, i)
                            for i in np.atleast_1d(self.idx)[idx]]).T

        rp = self.rotor_position
        if len(np.shape(rp)) == 2:
            rp = rp[:, list(np.atleast_1d(self.idx)).index(idx)]
        # x,y,z is floats (not arrays) but get_windspeed returns a list, so extract for first position
        return self.flowSimulation.get_windspeed(rp, include_wakes=include_wakes, exclude_wake_from=[idx])[:, 0]

    def rotor_avg_ti(self, idx=slice(None)):
        # TODO: Change to effective TI instead of ambient???
        if not isinstance(idx, (int, np.integer)):
            return np.array([self.rotor_avg_ti(i)
                            for i in np.atleast_1d(self.idx)[idx]]).T

        rp = self.rotor_position
        if len(np.shape(rp)) == 2:
            rp = rp[:, list(np.atleast_1d(self.idx)).index(idx)]
        return self.flowSimulation.get_turbulence_intensity(rp, False)[0]

    @abstractmethod
    def ct(self, idx=slice(None)):
        ""

    @abstractmethod
    def power(self, include_wakes=True, idx=slice(None),):
        ""

    @abstractmethod
    def rotor_avg_induction(self, idx=slice(None)):
        ""

    @abstractmethod
    def axisymetric_induction(self, idx=slice(None)):
        ""

    @abstractmethod
    def yaw_tilt(self):
        ""
