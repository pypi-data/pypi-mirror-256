from py_wake.deficit_models.gaussian import NiayifarGaussianDeficit
from py_wake.examples.data.hornsrev1 import V80
from dynamiks.dwm.particle_deficit_profiles.pywake_deficit_wrapper import PyWakeDeficitGenerator
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import MannTurbulenceField
from dynamiks.utils.test_utils import tfp, DefaultDWMFlowSimulation
from dynamiks.views import XYView, XZView, YView, YZView, XView
from dynamiks.visualizers.flow_visualizers import Flow2DVisualizer, Flow, Flow1DVisualizer
from dynamiks.visualizers.visualizer_utils import InteractiveFigure, AxesInitializer, ParticleVisualizer
from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines
import matplotlib.pyplot as plt
import pytest
from pathlib import Path
import matplotlib


def test_flow_visualizer():
    if matplotlib.get_backend() == 'agg':
        pytest.xfail("agg backend")

    ws = 10
    ti = .06
    x, y = [0, 400], [0, 0]

    turbfield = MannTurbulenceField.from_netcdf(tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_3.200x3.20x3.20_s0001.nc",
                                                offset=(-2500, -100, 20))
    turbfield.scale_TI(ti=ti, U=ws)
    turbfield.uvw[:, :3] = 5
    turbfield.uvw[:, :, :3] = 5
    turbfield.uvw[:, :, :, :3] = 5
    site = TurbulenceFieldSite(ws=ws, ti=.1, turbulenceField=turbfield)

    wt = PyWakeWindTurbines(x, y, V80())
    deficit_model = NiayifarGaussianDeficit()

    fig = InteractiveFigure(figsize=(10, 8))

    ax1, ax2, ax3, ax4, ax5 = fig.subplots(5)

    xy_view = XYView(z=70, ax=ax1)
    xy_flow2DVisualizer = Flow2DVisualizer(flow2d=Flow(uvw='u', include_wakes=True), view=xy_view)

    xz_view = XZView(y=0, ax=ax2)
    xz_flow2DVisualizer = Flow2DVisualizer(flow2d=Flow(uvw='u', include_wakes=True), view=xz_view)

    yz_view = YZView(x=200, ax=ax3)
    yz_flow2DVisualizer = Flow2DVisualizer(flow2d=Flow(uvw='u', include_wakes=True), view=yz_view)

    x_view = XView(y=0, z=70, ax=ax4)
    x_flow1DVisualizer = Flow1DVisualizer(flow=Flow(uvw='u', include_wakes=True), view=x_view)

    y_view = YView(x=200, z=70, ax=ax5)
    y_flow1DVisualizer = Flow1DVisualizer(flow=Flow(uvw='u', include_wakes=True), view=y_view)

    step_handlers = [
        AxesInitializer(ax=ax1, axis='scaled', ylabel='y [m]', xlabel='x [m]'),
        AxesInitializer(ax=ax2, axis='scaled', ylabel='z [m]', xlabel='x [m]'),
        AxesInitializer(ax=ax3, axis='scaled', title='x=200', ylabel='z [m]', xlabel='y [m]'),
        lambda _: ax1.axvline(200, color='k', ls='--'),
        lambda _: ax2.axvline(200, color='k', ls='--'),

        AxesInitializer(ax=ax4, title='y=0, z=70', ylabel='u [m/s]', xlabel='x [m]'),
        AxesInitializer(ax=ax5, title='x=200, z=70', ylabel='u [m/s]', xlabel='y [m]'),

        xy_flow2DVisualizer,
        xz_flow2DVisualizer,
        yz_flow2DVisualizer,
        x_flow1DVisualizer,
        y_flow1DVisualizer,

        ParticleVisualizer(True, xy_view),
        xy_view.get_plot_windturbines(),
        xz_view.get_plot_windturbines(),
        yz_view.get_plot_windturbines(),
        fig
    ]

    fs = DefaultDWMFlowSimulation(x, y, ws=ws, ti=ti, site=site, windTurbines=wt,
                                  wakeDeficitModel=PyWakeDeficitGenerator(deficitModel=deficit_model),
                                  dt=1, fc=0.1, d_particle=2, n_particles=10)
    fs.add_step_handlers(step_handlers, t0=50, dt=None)
    fs.run(53)
    if 0:
        fs.run(153)
        plt.show()
    plt.close('all')


def test_flowsimulation_visualize():
    if matplotlib.get_backend() == 'agg':
        pytest.xfail("agg backend")
    x, y = [0, 400], [0, 0]
    fs = DefaultDWMFlowSimulation(x=x, y=y, wd=0)

    fs.run(100)
    fs.visualize(102, dt=1)
    if 0:
        plt.show()
    plt.close('all')


def test_animation():
    if matplotlib.get_backend() == 'agg':
        pytest.xfail("agg backend")
    x, y = [0, 400], [0, 0]
    fs = DefaultDWMFlowSimulation(x=x, y=y)
    fs.run(100)
    for ext in ['.gif', '.avi']:
        f = Path(tfp + f'tmp{ext}')
        f.unlink(missing_ok=True)
        fs.animate(fs.time + 3, filename=f, verbose=False)
        assert f.exists()

    plt.close('all')


def test_increase_coverage():
    fig = InteractiveFigure()
    fig.clf()
    fig.subplots(1, 1)

    def update(_):
        plt.gcf().canvas.draw()
        plt.gcf().canvas.flush_events()

    fs = DefaultDWMFlowSimulation(x=[0, 400], y=[0, 0], site='mann', step_handlers=[
        AxesInitializer(title='y=0, z=70', ylabel='u [m/s]', xlabel='x [m]', xlim=[-500, 1000], ylim=[-3, 13]),
        Flow1DVisualizer(view=XView(y=0, z=70)),
        update
    ])
    fs.run(10)
    if 0:
        fs.run(110)
        plt.show()
    plt.close('all')
