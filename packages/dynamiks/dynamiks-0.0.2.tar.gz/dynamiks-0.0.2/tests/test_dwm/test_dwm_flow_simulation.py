import time

import pytest

from dynamiks.dwm.added_turbulence_models import AutoScalingIsotropicMannTurbulence,\
    SynchronizedAutoScalingIsotropicMannTurbulence
from dynamiks.utils.data_dumper import DataDumper
from dynamiks.utils.test_utils import npt, DefaultDWMFlowSimulation, tfp
from dynamiks.views import Grid3D, YView

from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines, ParallelPyWakeWindTurbines
import matplotlib.pyplot as plt
import numpy as np
from py_wake.utils.plotting import setup_plot
import xarray as xr
from py_wake.wind_turbines._wind_turbines import WindTurbines
from py_wake.examples.data.hornsrev1 import V80
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
from dynamiks.wind_turbines.hawc2_windturbine import HAWC2FreeWindWindTurbinesDummy
from tests.test_windturbines.test_windturbines import get_site
from dynamiks.dwm.particles_model import DistributedWindTurbinesParticles, WindTurbinesParticles
from py_wake.utils.layouts import rectangle
from dynamiks.sites.turbulence_fields import MannTurbulenceField
from dynamiks.sites._site import TurbulenceFieldSite


def test_windspeed_and_production():
    ws_dumper = DataDumper(data_dumper_function=lambda fs:
                           [[fs.windTurbines.rotor_avg_windspeed(idx=wt, include_wakes=wakes)[0]
                             for wakes in [False, True]] for wt in [0, 1, 2]],
                           coords={'wt': [0, 1, 2], 'wakes': [False, True]})

    power_dumper = DataDumper(data_dumper_function=lambda fs: [[fs.windTurbines.power(wakes, wt)
                                                                for wakes in [False, True]] for wt in [0, 1, 2]],
                              coords={'wt': [0, 1, 2], 'wakes': [False, True]})

    def sleep_step_handler(fs):
        time.sleep(0.1)

    step_handlers = [ws_dumper, power_dumper, sleep_step_handler]

    fs = DefaultDWMFlowSimulation(x=[-5 * 80, 0, 80 * 5], y=[0, 0, 0], site='mann', step_handlers=step_handlers,
                                  addedTurbulenceModel=None)

    fs.step_handler_time = {}
    fs.step()
    da = power_dumper.to_xarray()  # test to_xarray with only one time stamp
    assert da.shape == (1, 3, 2)
    # fs.visualize(100)

    fs.run(10)
    npt.assert_allclose(fs.step_handler_time[sleep_step_handler], fs.time * 0.1, atol=0.1)
    fs.step_handlers.remove(sleep_step_handler)

    fs.run(101)
    fs.step()
    ws = ws_dumper.to_xarray()
    power = power_dumper.to_xarray() / 1000
    if 0:
        for t, da in [('ws', ws), ('Power', power)]:
            plt.figure()
            for wt in da.wt:
                c = plt.plot(da.sel(wt=wt, wakes=False), label=f'wt {wt.item()}')[0].get_color()
                plt.plot(da.sel(wt=wt, wakes=True), '--', color=c)
            setup_plot(title=t)
            plt.show()

    npt.assert_allclose((ws.sel(wakes=True) / ws.sel(wakes=False)).min('time'), [1., 0.680968, 0.691742], atol=0.001)
    npt.assert_allclose((ws.sel(wakes=True) / ws.sel(wakes=False))
                        [60:].max('time'), [1., 0.895994, 0.792806], atol=0.001)

    # wake_loss (max, min and mean)
    eff = power.sel(wakes=True) / power.sel(wakes=False)
    npt.assert_allclose(1 - eff.min('time'), [0., 0.698634, 0.669175], atol=0.001)
    npt.assert_allclose(1 - eff[60:].max('time'), [0., 0.207414, 0.427925], atol=0.002)
    npt.assert_allclose(1 - eff[60:].mean('time'), [0., 0.452346, 0.557304], atol=0.001)


def test_no_upstream_deficit():
    fs = DefaultDWMFlowSimulation(x=[0, 80 * 5], y=[0, 0], site='mann', addedTurbulenceModel=None)
    fs.run(10)
    ref_uvw = fs.get_windspeed([0, 0, 70], include_wakes=False, exclude_wake_from=[])
    npt.assert_array_equal(ref_uvw, fs.get_windspeed([0, 0, 70], include_wakes=True, exclude_wake_from=[0]))

    grid = Grid3D(x_slice=slice(749, 752), y_slice=slice(31, 33), z_slice=slice(15, 17),
                  axes=fs.site.turbulenceField.get_axes(fs.time))
    uvw = fs.get_windspeed(grid, include_wakes=True, exclude_wake_from=[0])
    da = xr.DataArray(uvw, dims=['uvw', 'x', 'y', 'z'],
                      coords={'uvw': ['u', 'v', 'w'], 'x': grid.x, 'y': grid.y, 'z': grid.z})
    npt.assert_array_almost_equal(ref_uvw[:, 0], da.interp(x=0, y=0, z=70))


@pytest.mark.parametrize('addedTurbulenceModel', [None, AutoScalingIsotropicMannTurbulence()])
def test_windspeed_grid(addedTurbulenceModel):
    fs = DefaultDWMFlowSimulation(x=[0, 80 * 5], y=[0, 0], ti=0.05, site='mann',
                                  addedTurbulenceModel=addedTurbulenceModel)
    fs.run(100)
    for exclude_wake_from in [[], [0], [1], [0, 1]]:
        for x in [-200, 200, 700]:
            x_idx = np.searchsorted(fs.site.turbulenceField.get_axes(fs.time)[0], x)
            grid = Grid3D(x_slice=slice(x_idx - 2, x_idx + 2), y_slice=slice(30, 33), z_slice=slice(14, 17),
                          axes=fs.site.turbulenceField.get_axes(fs.time))
            uvw = fs.get_windspeed(grid, include_wakes=True, exclude_wake_from=exclude_wake_from, xarray=True)
            xp, yp, zp = grid.x[0], grid.y[0], grid.z[0]
            ref_uvw = fs.get_windspeed([xp, yp, zp], include_wakes=True, exclude_wake_from=exclude_wake_from)
            npt.assert_array_almost_equal(ref_uvw[:, 0], uvw.interp(x=xp, y=yp, z=zp))


@pytest.mark.parametrize('wd,ref_xy', [(270, [(0, 200, 0, -200), (0, 0, 100, -100)]),
                                       (0, [(0, 0, -100, 100), (0, 200, 0, -200)]),
                                       (240, [(0, 2 * 86.60, 50, -223.21), (0, -2 * 50, 86.60, 13.4)])])
def test_wind_direction(wd, ref_xy):
    fs = DefaultDWMFlowSimulation(x=[0, 200, 0, -200], y=[0, 0, 100, -100], wd=wd)
    npt.assert_array_almost_equal(fs.rotor_positions[:2, :], ref_xy, 2)


@pytest.mark.parametrize('windTurbines', [
    lambda: PyWakeWindTurbines(x=[0, 0, 0], y=[0, 500, 1000],
                               windTurbine=WindTurbines.from_WindTurbine_lst([
                                   V80(),
                                   GenericWindTurbine(name='G100', diameter=100, hub_height=80, power_norm=2300)])),
    lambda: HAWC2FreeWindWindTurbinesDummy(x=[0, 0, 0], y=[0, 500, 1000], htc_filename_lst=[''], types=[0], site=get_site(),
                                           windfield_update_interval=5, suppress_output=True)])
def test_combinations(windTurbines):
    fs = DefaultDWMFlowSimulation(windTurbines=windTurbines())
    atm_lst = [SynchronizedAutoScalingIsotropicMannTurbulence(),
               AutoScalingIsotropicMannTurbulence()]
    for atm in atm_lst:
        fs.addedTurbulenceModel = atm
        fs.run(6)


def test_turbulence_intensity():
    fs = DefaultDWMFlowSimulation()

    ti = fs.get_turbulence_intensity(YView(x=500, z=70, y=[0, 10], adaptive=False), include_wake_turbulence=False)
    npt.assert_array_equal(ti, [0.1, 0.1])


@pytest.mark.parametrize('windTurbineParticles_cls', [
    # WindTurbinesParticles, # only needed to ensure eq when recalculating ref
    DistributedWindTurbinesParticles])
@pytest.mark.parametrize('windTurbines_cls', [ParallelPyWakeWindTurbines, HAWC2FreeWindWindTurbinesDummy])
def test_distributed_wt_particles(windTurbineParticles_cls, windTurbines_cls):
    N = 4
    D = 80
    ws = 10
    ti = 0.1
    x, y = rectangle(N, columns=np.sqrt(N), distance=5 * D)
    turbfield = MannTurbulenceField.from_netcdf(
        tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_3.200x3.20x3.20_s0001.nc",
        offset=(-2500, -100, 20))
    turbfield.scale_TI(ti=ti, U=ws)
    site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)
    if windTurbines_cls == ParallelPyWakeWindTurbines:
        windTurbines = windTurbines_cls(x, y, windTurbine=V80())
        ref = [11.0, 10.6, 8.7, 8.1, 6.8, 8.5, 10.0, 11.6, 11.6, 10.1, 12.3, 10.7, 10.3, 10.7,
               10.6, 10.9, 8.9, 7.2, 6.3, 7.9, 9.0]
    elif windTurbines_cls == HAWC2FreeWindWindTurbinesDummy:
        from h2lib_tests import tfp as h2_tfp
        fn = [h2_tfp + 'DTU_10_MW/htc/DTU_10MW_RWT.htc']
        windTurbines = windTurbines_cls(x=x, y=y, htc_filename_lst=fn, types=[0], site=site,
                                        windfield_update_interval=5,
                                        suppress_output=True)
        ref = [10.3, 9.1, 6.9, 7.3, 5.5, 6.5, 8.8, 11.1, 11.5, 10.1,
               12.3, 10.7, 10.2, 10.3, 9.3, 8.2, 5.3, 4.5, 2.7, 3.9, 6.5]

    fs = DefaultDWMFlowSimulation(
        site=site,
        windTurbines=windTurbines,
        windTurbineParticles_cls=windTurbineParticles_cls)
    fs.run(10)

    u = fs.get_windspeed(YView(x=600, z=70, y=np.linspace(-100, 500, 20)), include_wakes=True)[0]
    if 0:
        print(np.round(u, 1).tolist())
        plt.plot(u)
        plt.figure()
        fs.visualize(fs.time + 2)
        plt.show()
    npt.assert_array_almost_equal(u, ref, 1)
