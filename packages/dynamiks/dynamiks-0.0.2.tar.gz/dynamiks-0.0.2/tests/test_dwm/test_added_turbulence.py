from dynamiks.dwm.added_turbulence_models import IsotropicMannTurbulence, AutoScalingIsotropicMannTurbulence,\
    SynchronizedAutoScalingIsotropicMannTurbulence
from dynamiks.utils.test_utils import DefaultDWMFlowSimulation, npt, tfp
from dynamiks.views import XYView, YView, Grid3D
import numpy as np
from dynamiks.visualizers.visualizer_utils import InteractiveFigure, AxesInitializer
from dynamiks.visualizers.flow_visualizers import Flow1DVisualizer, Flow2DVisualizer, Flow
import pytest
import matplotlib.pyplot as plt
from pathlib import Path
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import MannTurbulenceField


@pytest.fixture(scope="session")
def delete_cache():
    Path('Hipersim_mann_l5.0_ae1.0000_g0.0_h0_128x128x128_1.562x0.62x0.62_s0001.nc').unlink(missing_ok=True)


@pytest.mark.parametrize("atm", [SynchronizedAutoScalingIsotropicMannTurbulence(),
                                 AutoScalingIsotropicMannTurbulence(),
                                 AutoScalingIsotropicMannTurbulence(),  # use saved file
                                 AutoScalingIsotropicMannTurbulence(cache_field=False),
                                 IsotropicMannTurbulence.generate(D=80),
                                 IsotropicMannTurbulence])
def test_IsotropicMannTurbulence(atm, delete_cache):
    D = 80
    U = 10
    ti = 0.1
    if atm == IsotropicMannTurbulence:
        atm = atm.from_netcdf(filename='Hipersim_mann_l5.0_ae1.0000_g0.0_h0_128x128x128_1.562x0.62x0.62_s0001.nc')
    if atm.__class__.__name__ == "IsotropicMannTurbulence":
        atm.scale(U=U)

    step_handlers = []
    turbfield = MannTurbulenceField.generate(offset=(0, 0, 0),
                                             dxyz=[1.5625, 0.625, 0.625], Nxyz=(32, 32, 32))
    turbfield.scale_TI(ti=0, U=U)
    site = TurbulenceFieldSite(ws=U, ti=ti, turbulenceField=turbfield)

    fs = DefaultDWMFlowSimulation(x=[-5 * D, 0, D * 5, D * 10], y=[0, 0, 0, 0], ws=U, ti=ti, site=site,
                                  addedTurbulenceModel=atm,
                                  step_handlers=step_handlers)
    if 0:
        fig = InteractiveFigure(figsize=(10, 8))
        ax1, ax2 = fig.subplots(2)

        view1d = YView(x=200, z=70, y=np.linspace(-200, 200, 500), adaptive=True, ax=ax2)
        view2d = XYView(z=70, x=np.linspace(-500, 500), y=np.linspace(-200, 200), adaptive=False, ax=ax1)
        flow_visualizer = Flow1DVisualizer(view=view1d)
        step_handlers = (fs._visualization_step_handlers(view=view2d, flowVisualizer=Flow2DVisualizer(),
                                                         particleVisualizer=False) +
                         [AxesInitializer(ax=ax2),
                          lambda fs:ax1.axvline(200),
                          flow_visualizer, fig])

        fs.step_handlers.extend(step_handlers)

    fs.run(100)
    view1d = YView(x=200, z=70, y=np.linspace(0, 10, 10), adaptive=False)
    # print(np.round(fs.get_windspeed_grid(grid=view1d, include_wakes=True)[0].squeeze(), 2).tolist())
    if isinstance(atm, SynchronizedAutoScalingIsotropicMannTurbulence):
        # SynchronizedAutoScalingIsotropicMannTurbulence has a random wt dependent offset
        ref = [4.79, 4.82, 5.05, 4.34, 3.77, 4.24, 4.36, 4.4, 4.32, 4.3]
    else:
        ref = [4.42, 4.74, 5.03, 5.46, 5.24, 4.9, 5.04, 4.79, 4.68, 4.72]
    if 0:
        plt.plot(view1d.y, fs.get_windspeed_grid(grid=view1d, include_wakes=True)[0].squeeze())
        plt.plot(view1d.y, ref, label='ref')
        plt.legend()
        plt.show()

    npt.assert_array_almost_equal(fs.get_windspeed(view1d, include_wakes=True)[0].squeeze(), ref, 2)

    npt.assert_array_almost_equal([fs.get_windspeed([view1d.x, y_, view1d.z], include_wakes=True)[0, 0]
                                   for y_ in view1d.y],
                                  ref, 2)

    axes = turbfield.get_axes(fs.time)
    grid3d = Grid3D(x_slice=slice(5, 6), y_slice=slice(0, 17), z_slice=slice(10, 11), axes=axes)
    grid1d = YView(x=grid3d.x, z=grid3d.z, y=grid3d.y, adaptive=False)
    npt.assert_array_almost_equal(fs.get_windspeed(grid3d, include_wakes=True)[0].squeeze(),
                                  fs.get_windspeed(grid1d, include_wakes=True)[0].squeeze())


def test_IsotropicMannTurbulence_ainslie():
    try:
        import jDWM
        from jDWM import EddyViscosityModel
        from dynamiks.dwm.particle_deficit_profiles.ainslie import jDWMAinslieGenerator
    except ModuleNotFoundError:
        pytest.xfail('jDWM not found')
    D = 80
    U = 10
    ti = .1

    atm = IsotropicMannTurbulence.generate(D)
    step_handlers = []
    fs = DefaultDWMFlowSimulation(x=[-5 * 80, 0, 80 * 5], y=[0, 0, 0], ws=U, ti=ti, site='uniform',
                                  wakeDeficitModel=jDWMAinslieGenerator(),
                                  addedTurbulenceModel=atm,
                                  step_handlers=step_handlers)
    if 0:
        fig = InteractiveFigure(figsize=(10, 8))
        ax1, ax2 = fig.subplots(2)

        view2d = XYView(z=70, x=np.linspace(-500, 500), y=np.linspace(-200, 200), adaptive=False, ax=ax1)
        view1d = YView(x=200, z=70, y=np.linspace(-200, 200, 500), adaptive=True, ax=ax2)
        flow_visualizer = Flow1DVisualizer(view=view1d)
        step_handlers = (fs._visualization_step_handlers(view=view2d, flowVisualizer=Flow2DVisualizer(), particleVisualizer=False) +
                         [AxesInitializer(ax=ax2),
                          flow_visualizer, fig])

        fs.step_handlers.extend(step_handlers)

    fs.run(100)
    view1d = YView(x=200, z=70, y=np.linspace(0, 10, 10), adaptive=True)
    # print(np.round(fs.get_windspeed_grid(grid=view1d, include_wakes=True)[0].squeeze(), 2).tolist())
    ref = [3.03, 3.48, 3.86, 4.44, 4.11, 3.61, 3.77, 3.4, 3.22, 3.22]
    if 0:
        plt.plot(view1d.y, fs.get_windspeed_grid(grid=view1d, include_wakes=True)[0].squeeze())
        plt.plot(view1d.y, ref, label='ref')
        plt.legend()
        plt.show()
    npt.assert_array_almost_equal(fs.get_windspeed(view1d, include_wakes=True)[0].squeeze(), ref, 2)
    npt.assert_array_almost_equal([fs.get_windspeed([200, y, 70], include_wakes=True)[0, 0] for y in view1d.y], ref, 2)


def test_deficit():
    U = 10
    ti = 0.1
    D = 80
    fs = DefaultDWMFlowSimulation(x=[-5 * 80, 0, 80 * 5], y=[0, 0, 0], ws=U, ti=ti, site='uniform',
                                  addedTurbulenceModel=IsotropicMannTurbulence.generate(D),
                                  )
    fs.run(100)
    if 0:
        fs.visualize(time_stop=200, dt=1,
                     view=XYView(z=70, x=np.linspace(-200, 500), y=np.linspace(-200, 200), adaptive=False),
                     flowVisualizer=Flow2DVisualizer(flow2d=Flow(uvw='v')))
    grid = YView(x=-100, z=70, y=np.linspace(-100, 100), adaptive=False)
    uvw = fs.get_windspeed(grid, include_wakes=True).squeeze()
    if 0:
        plt.plot(grid.y, uvw[1])
        plt.show()
    npt.assert_allclose(uvw.mean(1), [8.54, 0, 0], atol=0.06)


if __name__ == '__main__':
    test_IsotropicMannTurbulence_ainslie()
