import numpy as np
import xarray as xr
from numpy import newaxis as na


class DataDumper():
    def __init__(self, data_dumper_function, coords={}, time_step_interval=1):
        self.data_dumper_function = data_dumper_function
        self.time_step_interval = time_step_interval
        self.coords = coords
        self.x = 500
        self.y = np.linspace(-200, 400, 1000)
        self.z = self.y * 0 + 70
        self.data = []
        self.time = []
        self.time_step = 0

    def __call__(self, flowSimulation):

        if self.time_step % self.time_step_interval == 0:
            self.data.append(self.data_dumper_function(flowSimulation))
            self.time.append(flowSimulation.time)
        self.time_step += 1

    def to_xarray(self):
        data = np.squeeze(self.data)
        if np.shape(self.data)[0] == 1:
            data = data[na]
        dims = ['time'] + list(self.coords.keys())
        dims.extend([f'dim_{i}' for i in range(len(dims), len(data.shape))])
        return xr.DataArray(data, dims=dims, coords={'time': self.time, **self.coords})
