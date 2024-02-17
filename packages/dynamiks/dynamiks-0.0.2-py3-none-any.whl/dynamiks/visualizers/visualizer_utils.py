import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
import os
from abc import abstractmethod, ABC
from tqdm import tqdm
from dynamiks.views import XYView, EastNorthView
from dynamiks.utils.geometry import get_east_north_height
from matplotlib.figure import Figure

# [plt.plot([])[0].get_color() for _ in range(10)]
color_lst = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf']


# class Figure():
#     def __init__(self, **fig_kw):
#         self.fig_kw = fig_kw
#
#     @property
#     def figure(self):
#         if not hasattr(self, '_figure'):
#             self._figure = plt.figure(**self.fig_kw)
#         return self._figure
#
#     @property
#     def axes(self):
#         return self.figure.axes
#
#     def __getattr__(self, name):
#         try:
#             return object.__getattr__(self, name)
#         except AttributeError:
#             if name == '_figure':
#                 raise
#             return getattr(self.figure, name)
#
#     def subplots(self, nrows=1, ncols=1, **fig_kw):
#         if hasattr(self, '_figure'):
#             plt.close(self._figure)
#         self._figure, axes = plt.subplots(nrows=nrows, ncols=ncols, **fig_kw)
#         return self._figure, axes
#
#         ""


class AnimationFigure():
    def __init__(self, fig=None, **fig_kw):
        plt.ioff()
        self.fig = fig or plt.figure(**fig_kw)
        self.gca = self.fig.gca
        self.subplots = self.fig.subplots
        self.clf = self.fig.clf

    def animate(self, flowSimulation, frames=100, interval=10, repeat=False, verbose=True):
        pbar = tqdm(total=frames, disable=not verbose)

        def step(index):
            if pbar.n <= index:
                pbar.update()
            flowSimulation.step()

        self.animation = FuncAnimation(self.fig, step, frames=frames,
                                       interval=interval, blit=False, repeat=repeat)
        return self.animation

    def __call__(self, fs):
        ""

    def save(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.gif':
            writergif = PillowWriter()
            self.animation.save(filename, writer=writergif)
        else:
            self.animation.save(filename, dpi=300)

    def show(self):
        plt.show()  # pragma: no cover


class InteractiveFigure():
    def __init__(self, fig=None, **fig_kw):
        plt.ion()
        self.fig = fig or plt.figure(**fig_kw)
        self.gca = self.fig.gca
        self.subplots = self.fig.subplots
        self.clf = self.fig.clf

    def __call__(self, flowSimulation):
        # for ax in self.fig.axes:
        #     if ax.get_xlim() == ax.get_ylim() == (-0.05500000000000001, 0.05500000000000001):
        #         ax.axis('scaled')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class AxesInitializer():
    def __init__(self, ax=None, xlabel=None, ylabel=None, title=None, xlim=None, ylim=None, axis='auto'):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        if ax is None:
            ax = plt.gca()
        self.ax = ax
        self.xlim = xlim
        self.ylim = ylim
        self.set_lim()
        self.axis = axis

    def set_lim(self):
        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        if self.ylim is not None:
            self.ax.set_ylim(self.ylim)

    def __call__(self, fs):
        self.ax.cla()
        if self.xlabel:
            self.ax.set_xlabel(self.xlabel)
        if self.ylabel:
            self.ax.set_ylabel(self.ylabel)
        if self.title:
            self.ax.set_title(self.title)
        else:
            self.ax.set_title(np.round(fs.time, 3))
        self.ax.axis(self.axis)
        self.set_lim()


class ParticleVisualizer():
    def __init__(self, deficit_profile=False, view=None):
        self.deficit_profile = deficit_profile
        if view:
            self.initialize(view)

    def initialize(self, view):
        self.xy_index = ['xyz'.index(c) for c in view.plane]
        self.view = view

    def __call__(self, flowSimulation):

        fs = flowSimulation

        # index of first, x, and second, y, axis
        ax = self.view.ax
        for i in range(fs.n_wt):
            c = color_lst[i % len(color_lst)]
            xy = fs.particle_positions_xip[self.xy_index, i]
            if isinstance(self.view, EastNorthView):
                xy = get_east_north_height([xy[0], xy[1], xy[0] * 0], fs.wind_direction, fs.center_offset)[:2]
            if self.deficit_profile:
                for j, (x, y) in enumerate(xy.T):
                    # TODO: 5x max(R)???
                    assert self.view.plane == 'xy', f'requested plane {self.view.plane} and only xy is implemented'
                    hcw = np.linspace(-5 * 40, 5 * 40)
                    deficit = fs.windTurbinesParticles[i].particles[0][j].get_profile(x, hcw, 0)

                    ax.plot(x + deficit * 10, y + hcw, color=c)

            x, y = xy[:, np.argsort(xy[0])]

            ax.plot(x, y, '.-', color=c)
