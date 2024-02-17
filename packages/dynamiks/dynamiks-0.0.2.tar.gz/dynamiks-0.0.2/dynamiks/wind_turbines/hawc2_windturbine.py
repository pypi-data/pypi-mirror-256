import numpy as np
from h2lib._h2lib import MultiH2Lib
from wetb.hawc2.htc_file import HTCFile
import os
from dynamiks.wind_turbines._windTurbines import WindTurbines
from numpy import newaxis as na
from dynamiks.views import Grid3D
import atexit
import inspect
from trace import PRAGMA_NOCOVER


def hawc2gl_to_uvw(xyz_gl, axis=0):
    xyz_gl = np.asarray(xyz_gl)
    return np.array([xyz_gl.take(1, axis), xyz_gl.take(0, axis), -xyz_gl.take(2, axis)])


def uvw_to_hawc2_gl(uvw, axis=0):
    return hawc2gl_to_uvw(uvw, axis)


class HAWC2WindTurbines(WindTurbines):
    def __init__(self, x, y, htc_filename_lst, types, case_name='', suppress_output=True):
        assert len(x) == len(y)
        WindTurbines.__init__(self, [os.path.basename(f) for f in htc_filename_lst], N=len(x))
        self.step_handlers.append(self.step)
        self.types = types = np.zeros(len(x), dtype=int) + types
        self.N = N = len(x)
        self.idx = np.arange(N)
        self.time = 0
        self.h2 = MultiH2Lib(N, suppress_output=suppress_output)
        self.dist_wt = self.h2
        htc_path_lst, model_path_lst = [], []
        for i, t in enumerate(types):
            htc = HTCFile(htc_filename_lst[t])
            htc.set_name(f'{os.path.splitext(os.path.basename(htc.filename ))[0]}_wt{i}', case_name)
            htc.save()
            model_path_lst.append(htc.modelpath)
            htc_path_lst.append(htc.filename)

        self.h2.read_input(htc_path_lst, model_path_lst)
        self.power_sensor = np.array(self.h2.add_sensor('aero power'))[:, 0]
        self.thrust_sensor = np.array(self.h2.add_sensor('aero thrust'))[:, 0]
        self.h2.init()
        z = np.zeros_like(x)
        self.position = np.array([x, y, z], dtype=float)
        self.init_rotor_variables()
        atexit.register(self.h2.close)

    def init_rotor_variables(self):
        self._rotor_position = self.h2.get_rotor_position()
        self._diameter = self.h2.get_diameter()

    @property
    def rotor_position(self):
        xyz = [np.atleast_1d(v) for v in np.transpose(self._rotor_position)]
        return hawc2gl_to_uvw(xyz, axis=0) + self.position

    def hub_height(self, idx=slice(None)):
        return -np.atleast_2d(self._rotor_position)[self.idx[idx], 2]

    def diameter(self, idx=slice(None)):
        return np.array(self.h2[idx].get_diameter())
        return np.atleast_1d(self._diameter)[self.idx[idx]]

    def step(self, flowSimulation):
        self.time = self.h2.run(flowSimulation.time)[0]
        self._rotor_position = self.h2.get_rotor_position()

    def __getitem__(self, idx):
        class WindTurbine():
            def __init__(self, windTurbines, idx):
                self.windTurbines = windTurbines
                if isinstance(idx, (int, np.int_)):
                    idx = [idx]
                self.idx = idx

            @property
            def rotor_position(self):
                return self.windTurbines.rotor_position[:, idx]

            def __getattr__(self, name):
                attr = getattr(self.windTurbines, name)
                argspec = inspect.getfullargspec(attr)
                if ((inspect.ismethod(attr) or inspect.isfunction(attr)) and
                        'idx' in argspec.args + argspec.kwonlyargs):
                    def wrap(*args, **kwargs):
                        return getattr(self.windTurbines, name)(*args, idx=self.idx, **kwargs)
                    return wrap
        return WindTurbine(self, idx)

    def rotor_avg_windspeed(self, include_wakes, idx=slice(None)):
        if include_wakes and self.time > 0:
            return np.array(self.h2[idx].get_rotor_avg_uvw()).T
        return WindTurbines.rotor_avg_windspeed(self, include_wakes, idx=idx)

    def ct(self, idx=slice(None), **_):
        # Tn = 1/2 rho ctn A (U cos theta)^2
        # ctx = ctn (cos theta)^2 = 2 Tn / (rho A U^2)
        T = np.array(self.h2[idx].get_sensor_values(self.thrust_sensor[idx].tolist())) * 1000
        A = np.pi * (self.diameter(idx=idx) / 2)**2
        U = np.array(self.rotor_avg_windspeed(include_wakes=True, idx=idx))[0]
        ct_x = 2 * T / (1.225 * A * U**2)
        return ct_x

    def power(self, include_wakes=True, idx=slice(None)):
        return np.array(self.h2[idx].get_sensor_values(self.power_sensor[idx].tolist()))

    def axisymetric_induction(self, r, idx=slice(None)):
        R_lst = np.array(self.diameter(idx)) / 2
        h2_r = self.h2[idx].get_bem_grid()[0][1]
        induc_lst = self.h2[idx].get_induction_axisymmetric()
        if h2_r[-1] == 0:
            return np.zeros((len(r), len(induc_lst)))
        for induc in induc_lst:
            induc[-1] = 0  # From HAWC2Farm, don't know why?
        return np.array([np.interp(r, h2_r / R, induc) for R, induc in zip(R_lst, induc_lst)]).T

    def rotor_avg_induction(self, idx=slice(None)):
        return np.array(self.h2[idx].get_induction_rotoravg())

    def yaw_tilt(self, idx=slice(None)):
        return np.array(self.h2[idx].get_rotor_orientation())[:, :2].T


class HAWC2FreeWindWindTurbines(HAWC2WindTurbines):
    def __init__(self, x, y, htc_filename_lst, types, site,
                 case_name='', windfield_update_interval=5, suppress_output=True):
        HAWC2WindTurbines.__init__(self, x, y, htc_filename_lst, types,
                                   case_name=case_name, suppress_output=suppress_output)
        self.init_windfield(site, update_interval=windfield_update_interval)

    def get_slice(self, ax, start, N):
        x0, dx = ax[0], ax[1] - ax[0]
        xi = int(np.floor((start - x0) / dx))

        if xi < 0 or xi + N > len(ax):
            # repeat box
            return np.arange(xi, xi + N)
        else:
            return slice(xi, xi + N)

    def init_windfield(self, site, update_interval=5):
        self.update_interval = update_interval
        Xs, Ys, Zs = site.turbulenceField.get_axes(0)
        dxyz = np.diff([Xs[:2], Ys[:2], Zs[:2]])
        D = self.diameter()
        # buffer size should be larger than rotor due to deflections and non-aligned grids
        Lx, Ly, Lz = (1.05 * D[na] + dxyz)
        Lz[:] = Zs[-1] - Zs[0]  # full box
        self.x_offset = update_interval * site.ws + Lx / 2
        Lx = update_interval * site.ws + Lx
        self.Nxyz = Nxyz = np.ceil(np.round([Lx, Ly, Lz] / dxyz + 1, 6)).astype(int)

        y, z = self.position[1:]
        yi = np.maximum(np.searchsorted(Ys, y - Ly / 2) - 1, 0)
        zi = np.maximum(np.searchsorted(Zs, z - Lz / 2) - 1, 0)
        box_offset_yz = np.array([Ys[yi] - y, Zs[:1] - z])
        self.y_slice_lst = [slice(yi_, yi_ + Ny) for yi_, Ny in zip(yi, Nxyz[1])]
        self.y_slice_lst = [self.get_slice(Ys, start, N) for start, N in zip(y - Ly / 2, Nxyz[1])]
        self.z_slice_lst = [slice(None)] * self.N

        self.h2.init_windfield(Nxyz=Nxyz.T.tolist(), dxyz=dxyz[:, 0],
                               box_offset_yz=box_offset_yz.T.tolist(), transport_speed=site.ws)
        grid_lst, box_offset_x_lst = self.get_grid(site)
        uvw_lst = [site.get_windspeed(grid) for grid in grid_lst]
        self.h2.set_windfield(uvw_lst, box_offset_x=box_offset_x_lst)
        self.last_windfield_update = - update_interval

    def get_grid(self, site):
        grid_lst = []
        box_offset_x_lst = []
        for x, x_offset, Nx, y_slice, z_slice in zip(self.position[0], self.x_offset, self.Nxyz[0],
                                                     self.y_slice_lst, self.z_slice_lst):
            axes = site.turbulenceField.get_axes(self.time)

            x_ax = axes[0]
            x0, dx = x_ax[0], x_ax[1] - x_ax[0]
            xi = int(np.floor((x - x_offset - x0) / dx))
            N = len(x_ax)
            if xi < 0 or xi + Nx > N:
                # repeat box
                x_slice = np.arange(xi, xi + Nx)
            else:
                x_slice = slice(xi, xi + Nx)
            x_slice = self.get_slice(axes[0], x - x_offset, Nx)
            grid_lst.append(Grid3D(x_slice, y_slice, z_slice, axes))
            box_offset_x_lst.append(xi * dx + x0 - x)

        return grid_lst, box_offset_x_lst

    def step(self, flowSimulation):
        import time
        if flowSimulation.time >= self.last_windfield_update + self.update_interval:
            t = time.time()
            site = flowSimulation.site
            # print('set new wind field')
            grid_lst, box_offset_x_lst = self.get_grid(site)
            uvw_lst = [flowSimulation.get_windspeed(grid, include_wakes=True, exclude_wake_from=[i])
                       for i, grid in enumerate(grid_lst)]
            self.h2.set_windfield(uvw_lst, box_offset_x=box_offset_x_lst)
            self.last_windfield_update = flowSimulation.time
            print('set windfield', flowSimulation.time, time.time() - t)
        HAWC2WindTurbines.step(self, flowSimulation)

    def get_windspeed(self, x, y, z):
        wt_x, wt_y, wt_z = self.position
        return np.array(self.h2.get_uvw(uvw_to_hawc2_gl([x - wt_x, y - wt_y, z - wt_z]).T.tolist())).T


def _get_dummy_diameter(*_, **__):  # pragma: no cover  # run in separate process
    return 178


def _get_dummy_rotor_position(*_, **__):  # pragma: no cover  # run in separate process
    return [0, 0, -119]


def _get_dummy_rotor_orientation(*_, **__):  # pragma: no cover  # run in separate process
    return [0, 0, 0]


class HAWC2FreeWindWindTurbinesDummy(HAWC2FreeWindWindTurbines):
    """Dummy wind turbine with same Dynamiks interface and behaviour as HAWC2FreeWindWindTurbines,
    but without HAWC2. Usefull to profiling the Dynamiks side of the HAWC2FreeWindWindTurbines interface"""

    def __init__(self, x, y, htc_filename_lst, types, site,
                 case_name='', windfield_update_interval=5, suppress_output=True):
        from h2lib_tests import tfp as h2_tfp
        htc_filename_lst = [h2_tfp + 'minimal/htc/minimal_nooutput.htc']
        HAWC2FreeWindWindTurbines.__init__(self, x, y, htc_filename_lst, types, site, case_name,
                                           windfield_update_interval, suppress_output)
        from dynamiks.wind_turbines.axisymetric_induction import InductionMatch
        self.inductionModel = InductionMatch()

    def init_rotor_variables(self):
        self.h2.get_diameter = _get_dummy_diameter
        self.h2.get_rotor_position = _get_dummy_rotor_position
        self.h2.get_rotor_orientation = _get_dummy_rotor_orientation
        HAWC2FreeWindWindTurbines.init_rotor_variables(self)

    def ct(self, idx=slice(None), **_):
        return np.full(self.N, 8 / 9)[idx]

    def rotor_avg_windspeed(self, include_wakes, idx=slice(None)):
        return WindTurbines.rotor_avg_windspeed(self, include_wakes, idx=idx)

    def axisymetric_induction(self, r, idx=slice(None)):
        tsr = 7
        from py_wake.deficit_models.utils import ct2a_madsen
        a_target_lst = ct2a_madsen(self.ct(idx=idx))
        return np.array([self.inductionModel(tsr=tsr, a_target=a_target, r=r)[1] for a_target in a_target_lst]).T

    def rotor_avg_induction(self, idx=slice(None)):
        from py_wake.deficit_models.utils import ct2a_madsen
        return ct2a_madsen(self.ct(idx=idx))
