from numpy import newaxis as na
from tqdm import tqdm
import matplotlib.pyplot as plt
from dynamiks.dwm.added_turbulence_models import SynchronizedAutoScalingIsotropicMannTurbulence

from dynamiks.views import XYView, Points, View
from dynamiks.visualizers.flow_visualizers import Flow2DVisualizer
from dynamiks.visualizers.visualizer_utils import InteractiveFigure, AxesInitializer, AnimationFigure, ParticleVisualizer
import numpy as np
import xarray as xr
import time
from py_wake.utils.model_utils import check_model
from dynamiks.dwm.particle_motion_models import ParticleMotionModel
from py_wake.superposition_models import LinearSum
from dynamiks.dwm.particles_model import WindTurbinesParticles

"""
suffixes:
u: uvw component
x: xyz component
i: wt
g: 1,2 or 3 grid dimensions
p: particle
"""
step_handler_time = {}


class DWMFlowSimulation():

    def __init__(self, site, windTurbines,
                 wakeDeficitModel, dt,
                 particleMotionModel,
                 d_particle=0.2, n_particles=100,
                 wind_direction=270,
                 step_handlers=None,
                 superpositionModel=LinearSum(),
                 addedTurbulenceModel=SynchronizedAutoScalingIsotropicMannTurbulence(),
                 windTurbinesParticles_cls=WindTurbinesParticles
                 ):
        self.n_particles = n_particles

        self.wakeDeficitModel = wakeDeficitModel
        self.superpositionModel = superpositionModel

        check_model(particleMotionModel, ParticleMotionModel, arg_name="particleMotionModel")
        self.particleMotionModel = particleMotionModel

        self.step_handlers = step_handlers or []

        windTurbines.flowSimulation = self
        self.n_wt = windTurbines.position.shape[1]
        self.windTurbines = windTurbines

        self.wind_direction = wind_direction

        self.site = site
        self.step_handlers = site.step_handlers + windTurbines.step_handlers + self.step_handlers
        self.dt = float(dt)
        wt_pos = windTurbines.positions_xyz(270, None)
        self.center_offset = (wt_pos.max(1) + wt_pos.min(1)) / 2
        self.time = 0

        site.initialize(self)

        self.particleMotionModel.initialize(self)
        if addedTurbulenceModel:
            addedTurbulenceModel.initialize(self)
        self.n_wt = n_wt = self.windTurbines.N
        self.wt_diameters = D = self.windTurbines.diameter()

        self.d_particle = d_particle * D
        # farm_size = np.hypot(*[xy - xy[:, na] for xy in wt_pos[:2]]).max()
        # assert np.all(self.d_particle * self.n_particles > farm_size)
        self.particle_positions_xip = (((np.arange(self.n_particles)[na] *
                                         self.d_particle[:, na])[na] *
                                        np.array([1., 0, 0])[:, na, na]) +
                                       self.rotor_positions[:, :, na])
        self.particle_velocity_uip = self.particleMotionModel.initial_speed(
        )[:, na, na] + np.zeros((3, n_wt, self.n_particles))

        self._last_particle_index = np.full(n_wt, -1, dtype=int)
        self.boundary_particle_index = np.zeros(n_wt, dtype=int)
        self._active_particles = np.full((n_wt, self.n_particles), False, dtype=bool)

        self.windTurbinesParticles = windTurbinesParticles_cls(
            windTurbines, n_particles, wakeDeficitModel, addedTurbulenceModel)
        self.kwargs_func = self.wakeDeficitModel.get_kwargs_func()

        for i in range(n_wt):
            kwargs = self.kwargs_func(self.windTurbines[i])
            self.windTurbinesParticles[i].reset_particle(0, self.particle_positions_xip[:, i, 0], kwargs)

    @property
    def rotor_positions(self):
        return self.windTurbines.rotor_positions_xyz(self.wind_direction, self.center_offset)

    @property
    def windturbine_positions(self):
        return self.windTurbines.positions_xyz(self.wind_direction, self.center_offset)

    def run(self, time_stop, verbose=False):
        steps = int(np.ceil(np.round((time_stop - self.time) / self.dt, 6)))
        for _ in tqdm(range(steps), disable=not verbose):
            self.step()

    def step(self):
        self.time = np.round(self.time + self.dt, 6)

        windturbine_positions = self.windturbine_positions
        rotor_positions = self.rotor_positions

        dx = (self.particle_positions_xip[0, np.arange(self.n_wt), (self.boundary_particle_index + 1) % self.n_particles] -
              windturbine_positions[0])  # could also be rotor_position
        m = (dx >= self.d_particle)

        if any(m):

            # emit old boundary particle
            for i, p in enumerate(self.boundary_particle_index):
                if m[i]:
                    if not self.particleMotionModel.update_initial_speed:
                        # reset particle speed to initial speed
                        self.particle_velocity_uip[:, i, p] = self.particleMotionModel.initial_speed(
                            self.windTurbines[i])

            # update boundary_particle_index
            self.boundary_particle_index[m] = (self.boundary_particle_index[m] - 1) % self.n_particles

            # reset new boundary particle
            for i, p in enumerate(self.boundary_particle_index):
                if m[i]:
                    kwargs = self.kwargs_func(self.windTurbines[i])
                    self.windTurbinesParticles[i].reset_particle(p, rotor_positions[:, i], kwargs)

                    # set new boundary particle speed (will update if update_initial_speed=True)
                    self.particle_positions_xip[:, i, p] = rotor_positions[:, i]
                    self.particle_velocity_uip[:, i, p] = self.particleMotionModel.initial_speed(self.windTurbines[i])

            self.particle_positions_xip[:, m, self.boundary_particle_index[m]] = rotor_positions[:, m]

        # propagate active particles
        self.particle_positions_xip, self.particle_velocity_uip = self.particleMotionModel(
            self.particle_positions_xip, self.particle_velocity_uip)

        # reset boundary particle position to windTurbine rotor positions
        self.particle_positions_xip[:,
                                    np.arange(self.n_wt),
                                    self.boundary_particle_index] = rotor_positions

        for step_handler in self.step_handlers:

            if isinstance(step_handler, tuple):
                (t0, dt), step_handler = step_handler
                if self.time > t0 and np.round(self.time / dt, 6) % 1 == 0:
                    for sh in np.atleast_1d(step_handler):
                        sh(self)
            else:
                if hasattr(self, 'step_handler_time'):
                    t = time.time()
                    step_handler(self)
                    self.step_handler_time[step_handler] = time.time() - t + self.step_handler_time.get(step_handler, 0)
                else:
                    step_handler(self)

    def add_step_handlers(self, step_handlers, t0, dt=None):
        self.step_handlers.append(((t0, dt or self.dt), step_handlers))

    def get_windspeed(self, xyz, include_wakes, exclude_wake_from=[], time=None, xarray=False):
        if isinstance(xyz, (list, tuple, np.ndarray)):
            view = Points(*xyz)
        else:
            view = xyz
        uvw = self.site.get_windspeed(view, time)

        if include_wakes:
            deficit = self.get_deficit(view, exclude_wake_from)
            uvw -= deficit
        if xarray:
            return xr.DataArray(uvw, dims=('uvw', 'x', 'y', 'z'),
                                coords={'uvw': ['u', 'v', 'w'], 'x': view[0], 'y': view[1], 'z': view[2]})
        else:
            return uvw

    def get_deficit(self, view, exclude_wake_from=[]):
        assert isinstance(view, View)
        x = view[0]
        src_wt_lst = np.array([i for i in np.arange(self.n_wt) if i not in exclude_wake_from])

        if len(src_wt_lst) == 0:
            return 0

        if len(np.unique(x)) == 1:
            x = float(np.unique(x)[0])

            # for each wt, find index of the particle before and after x
            px = self.particle_positions_xip[0, src_wt_lst]
            # index of most downstream particle (particles downstream of x are set far upstream)
            i0 = np.argmax(px - (px > x) * 1e10, 1)
            i1 = np.argmin(px + (px < x) * 1e10, 1)

            # exclude wt if first particle is downstream of x or last particle is upstream of x
            i_ = np.arange(len(src_wt_lst))
            m = (px[i_, i0] <= x) & (px[i_, i1] >= x)
            if np.any(m):
                src_wt_lst = src_wt_lst[m]
                i0, i1 = i0[m], i1[m]
            else:
                return 0
            mask_ip = np.array([i0, i1]).T.tolist()
        else:
            def get_mask(src_wt):
                px = self.particle_positions_xip[0, src_wt]
                j = np.argsort(px)
                idx = np.searchsorted(px[j], x)
                low = np.minimum(np.maximum(np.unique(idx) - 1, 0), len(px) - 2)
                high = np.minimum(np.maximum(np.unique(idx), 1), len(px) - 1)
                idx = sorted(np.unique(np.r_[low, high]))
                return j[idx]
            mask_ip = [get_mask(src_wt) for src_wt in src_wt_lst]

        deficit_iug = self.windTurbinesParticles[src_wt_lst].get_deficit(
            view, [self.particle_positions_xip[:, i] for i in src_wt_lst], mask_ip,
            self.time, self.rotor_positions[:, src_wt_lst].T.tolist())
        return self.superpositionModel(deficit_iug)

    def get_turbulence_intensity(self, xyz, include_wake_turbulence):
        if isinstance(xyz, (list, tuple, np.ndarray)):
            view = Points(*xyz)
        else:
            view = xyz
        return self.site.get_turbulence_intensity(view)

    def _visualization_step_handlers(self, view,
                                     flowVisualizer,
                                     particleVisualizer):

        flowVisualizer.initialize(view)

        step_handlers = [AxesInitializer(ax=view.ax, xlim=view.xlim, ylim=view.ylim, axis='scaled'), flowVisualizer,
                         view.get_plot_windturbines()]
        if particleVisualizer:
            particleVisualizer.initialize(view)
            step_handlers.append(particleVisualizer)

        return step_handlers

    def visualize(self, time_stop, dt=None, view=None,
                  flowVisualizer=None,
                  particleVisualizer=None):
        view = view or XYView(z=self.windTurbines.hub_height(self.windTurbines.types).mean())
        if flowVisualizer is None:
            flowVisualizer = Flow2DVisualizer()
        if particleVisualizer is None:
            particleVisualizer = ParticleVisualizer()
        with plt.ion():
            if view and view.ax:
                fig = InteractiveFigure(view.ax.figure)

            step_handlers = self._visualization_step_handlers(view=view, flowVisualizer=flowVisualizer,
                                                              particleVisualizer=particleVisualizer)
            step_handlers.append(fig)
            if dt is not None:
                step_handlers = [((0, dt), step_handlers)]
            self.step_handlers += step_handlers
            try:
                self.run(time_stop)
            finally:
                for sh in step_handlers:
                    self.step_handlers.remove(sh)

        return fig

    def animate(self, time_stop, filename=None,
                view=None, flowVisualizer=None, particleVisualizer=None, verbose=True):
        view = view or XYView(z=self.windTurbines.hub_height(self.windTurbines.types).mean())
        if flowVisualizer is None:
            flowVisualizer = Flow2DVisualizer()
        if particleVisualizer is None:
            particleVisualizer = ParticleVisualizer()
        with plt.ioff():
            if view and view.ax:
                fig = AnimationFigure(view.ax.figure)

        step_handlers = self._visualization_step_handlers(view=view, flowVisualizer=flowVisualizer,
                                                          particleVisualizer=particleVisualizer)
        time_steps = int(np.ceil((time_stop - self.time) / self.dt))
        self.step_handlers += step_handlers
        try:
            fig.animation = fig.animate(self, frames=time_steps, interval=self.dt * 1000, repeat=False, verbose=verbose)
            if filename:
                fig.save(filename)
            else:  # pragma: no cover
                try:
                    assert get_ipython().__class__.__name__ == 'ZMQInteractiveShell'  # @UndefinedVariable
                    fig = fig.animation.to_jshtml()
                except (NameError, AssertionError):
                    fig.show()
        finally:
            for sh in step_handlers:
                self.step_handlers.remove(sh)
        return fig
