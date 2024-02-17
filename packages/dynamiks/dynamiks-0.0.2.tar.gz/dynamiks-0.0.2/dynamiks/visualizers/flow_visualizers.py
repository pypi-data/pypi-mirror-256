import matplotlib.pyplot as plt
from dynamiks.utils.geometry import get_xyz


class Flow():
    def __init__(self, uvw='u', include_wakes=True):
        self.comp = 'uvw'.index(uvw)
        self.include_wakes = include_wakes

    def __call__(self, flowSimulation, view):
        return flowSimulation.get_windspeed(view, self.include_wakes)[self.comp]


class Flow2DVisualizer():
    def __init__(self, flow2d=Flow(), levels=50, color_bar=True, view=None):
        self.levels = levels
        self.color_bar = color_bar
        self.flow2d = flow2d
        if view:
            self.initialize(view)

    def initialize(self, view):
        self.view = view

    def __call__(self, flowSimulation):
        flow = self.flow2d(flowSimulation, self.view).T

        X, Y = self.view.XY(flowSimulation.wind_direction, flowSimulation.center_offset)
        c = self.view.ax.contourf(X, Y, flow, levels=self.levels)
        if self.color_bar:
            try:
                self.cb.remove()
            except BaseException:
                pass
            self.cb = plt.colorbar(c, ax=self.view.ax)


class Flow1DVisualizer(Flow2DVisualizer):
    def __init__(self, flow=Flow(), view=None):
        self.initialize(view)
        self.flow = flow

    def __call__(self, flowSimulation):
        flow = self.flow(flowSimulation, self.view)
        self.view.ax.plot(self.view.X, flow)
