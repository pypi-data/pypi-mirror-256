from dynamiks.utils.data_dumper import DataDumper
from dynamiks.visualizers.visualizer_utils import AxesInitializer, InteractiveFigure, ParticleVisualizer
from dynamiks.dwm.flow_simulation import DWMFlowSimulation
from dynamiks.dwm.particle_deficit_profiles.pywake_deficit_wrapper import PyWakeDeficitGenerator
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import RandomTurbulence
from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines
import matplotlib.pyplot as plt
import numpy as np
from py_wake.deficit_models.fuga import FugaDeficit
from py_wake.deficit_models.gaussian import BastankhahGaussianDeficit, NiayifarGaussianDeficit
from py_wake.examples.data.hornsrev1 import V80
from dynamiks.views import XYView, YView, Points
from dynamiks.utils.test_utils import npt, DefaultDWMFlowSimulation
from dynamiks.visualizers.flow_visualizers import Flow1DVisualizer
from dynamiks.dwm.added_turbulence_models import AutoScalingIsotropicMannTurbulence
import pytest
from dynamiks.dwm.particle_motion_models import ParticleMotionModel


def test_pywake_wrapper():
    plot = 0
    ws = 10
    x, y = [0, 0, 0, 100], [0, 300, 200, 50]
    turbfield = RandomTurbulence(ti=0, ws=10)
    site = TurbulenceFieldSite(ws=ws, ti=.1, turbulenceField=turbfield)

    wt = PyWakeWindTurbines(x, y, V80())
    deficit_model = FugaDeficit()

    step_handlers = []
    ref = [0.0, 0.0, 0.0, 0.0, 0.0, 0.128, 0.435, 0.958, 1.699, 2.148, 2.471, 2.483, 2.482,
           2.472, 2.493, 2.494, 2.482, 2.489, 2.495, 2.488]
    if plot:
        px = 500
        py = np.linspace(-200, 400, 1000)
        pz = py * 0 + 70

        ifig = InteractiveFigure(figsize=(10, 8))

        ax1, ax2, ax3 = ifig.subplots(1, 3)

        y_lst = np.arange(-200, 400, 10)

        def draw(fs):
            ax3.plot(tsd.time, tsd.data)
            ax1.plot(y_lst * 0 + 500, y_lst, '--k')
            ax1.plot(500, 0, '.k')
            ax3.plot(np.arange(1, 97, 5), ref, 'xk')

        view1 = XYView(y=None, z=None, ax=ax1, xlim=[-100, 800])
        step_handlers = [
            AxesInitializer(ax=ax1, xlim=[-100, 800], ylim=None),
            AxesInitializer(ax=ax2, ylim=[5, 11]),
            AxesInitializer(ax=ax3, ylim=[-.1, 3]),
            Flow1DVisualizer(view=YView(x=500, z=70, y=y_lst, ax=ax2)),
            ParticleVisualizer(True, view1),
            draw,
            ifig,
        ]

    tsd = DataDumper(data_dumper_function=lambda fs: fs.get_deficit(Points(500, 0, 70))[0], coords={})
    step_handlers.append(tsd)

    fs = DWMFlowSimulation(site, windTurbines=wt, dt=1,
                           wakeDeficitModel=PyWakeDeficitGenerator(deficitModel=deficit_model),
                           d_particle=2,
                           n_particles=10,
                           addedTurbulenceModel=None,
                           particleMotionModel=ParticleMotionModel(cut_off_frequency=0.1),
                           step_handlers=step_handlers
                           )

    fs.run(100, verbose=False)

    # print(list(np.round(np.squeeze(tsd.data[::5]), 3)))
    npt.assert_array_almost_equal(np.squeeze(tsd.data[::5]),
                                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.122, 0.415, 0.925, 1.656, 2.105, 2.427, 2.439, 2.402,
                                   2.358, 2.348, 2.337, 2.327, 2.334, 2.341, 2.333], 3)


def test_profiles():
    plot = 0
    ws = 10
    ti = .12
    x, y = [0, 0, 0, 100], [0, 300, 200, 50]

    step_handlers = []
    py = np.linspace(-200, 400, 1000)
    px = py * 0 + 500
    pz = py * 0 + 70

    deficit_generator_lst = [
        ('Fuga', PyWakeDeficitGenerator(deficitModel=FugaDeficit()),
         [-0.05, -0.04, -0.02, 0.06, 0.35, 0.96, 1.82, 2.51, 2.55, 1.9, 1.1, 0.81, 1.15, 1.61, 1.75, 1.73, 1.75, 1.59, 1.06, 0.47]),
        ('Bastankhah', PyWakeDeficitGenerator(deficitModel=BastankhahGaussianDeficit()),
         [0.0, 0.0, 0.0, 0.03, 0.26, 1.14, 2.84, 4.49, 5.01, 3.45, 1.28, 0.65, 1.58, 2.78, 2.68, 2.19, 2.7, 2.76, 1.52, 0.43]),
        ('Niayifar', PyWakeDeficitGenerator(deficitModel=NiayifarGaussianDeficit()),
         [0.0, 0.0, 0.01, 0.09, 0.36, 1.03, 2.06, 3.08, 3.4, 2.55, 1.32, 0.84, 1.24, 1.79, 1.92, 1.84, 1.92, 1.77, 1.16, 0.5])]

    try:
        import jDWM
        from jDWM import EddyViscosityModel
        from dynamiks.dwm.particle_deficit_profiles.ainslie import jDWMAinslieGenerator
        deficit_generator_lst.append(
            ('ainslie', jDWMAinslieGenerator(),
             [0.0, 0.0, 0.0, 0.0, 0.06, 1.13, 3.82, 6.2, 6.32, 4.01, 1.02, 0.23, 2.0, 4.22, 3.72, 2.25, 3.77, 4.19, 1.92, 0.18]))
    except ModuleNotFoundError:
        pass

    for l, deficit_generator, ref in deficit_generator_lst:

        fs = DefaultDWMFlowSimulation(x, y, ws=ws, ti=ti, site='random', wakeDeficitModel=deficit_generator,
                                      step_handlers=step_handlers)
        fs.run(100)

        deficit = fs.get_deficit(Points(px, py, pz))[0]
        if plot:
            plt.xlim([-100, 800])
            c = plt.plot(deficit * 10 + px, py, label=l)[0].get_color()
            plt.plot(deficit[::50] * 10 + px, py[::50], '.', color=c)
            print(list(np.round(deficit[::50], 2)))

        #npt.assert_array_almost_equal(ref, deficit[::50], 2)

    if plot:
        XYView(z=70).plot_windturbines(fs)
        plt.axvline(px, color='k', ls=':')
        plt.legend()
        plt.show()


def test_ainslie():
    try:
        import jDWM
    except ModuleNotFoundError:
        pytest.xfail("jDWM not present")
    from jDWM import EddyViscosityModel
    from dynamiks.dwm.particle_deficit_profiles.ainslie import jDWMAinslieGenerator

    fs = DefaultDWMFlowSimulation(
        x=[0, 400], y=[0, 0],
        dt=0.01,
        wakeDeficitModel=jDWMAinslieGenerator(),
        addedTurbulenceModel=AutoScalingIsotropicMannTurbulence(),

    )
    # new boundary particle 1m downstream of wt1
    fs.windTurbines.rotor_position[0, 1] = 401
    fs.d_particle = 0
    fs.step()
    fs.windTurbines.rotor_position[0, 1] = 400
    fs.d_particle = 160
    # failed previously when trying to calculate deficit profile upstream of boundary particle initial position
    fs.run(20)


if __name__ == '__main__':
    test_profiles()
