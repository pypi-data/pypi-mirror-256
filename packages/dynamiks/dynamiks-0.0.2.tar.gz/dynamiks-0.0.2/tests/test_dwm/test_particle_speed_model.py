from dynamiks.dwm.particle_deficit_profiles.pywake_deficit_wrapper import PyWakeDeficitGenerator
from dynamiks.dwm.particle_motion_models import ParticleMotionModel, HillVortexParticleMotion, CutOffFrqLarsen2008
from dynamiks.utils.test_utils import DefaultDWMFlowSimulation, npt
from dynamiks.views import XYView
import matplotlib.pyplot as plt
import numpy as np
from py_wake.deficit_models.gaussian import BastankhahGaussianDeficit

import pytest


def test_update_initial_speed():
    class MyPSM(ParticleMotionModel):
        def initial_speed(self, windTurbine=None):
            return np.array([5])

    psm = MyPSM(CutOffFrqLarsen2008, update_initial_speed=False)
    fs = DefaultDWMFlowSimulation(particleMotionModel=psm, dt=0.01, d_particle=.1)
    fs.step()
    while fs.particle_positions_xip[0, 0, -1] == 0:
        fs.step()  # run until new particle is emitted

    npt.assert_allclose(fs.particle_velocity_uip[0, 0, -1], 5, atol=0.03)


def test_deflection_pywake_deficit():
    fs = DefaultDWMFlowSimulation(x=[0, 0], y=[0, 200], particleMotionModel=HillVortexParticleMotion(CutOffFrqLarsen2008),
                                  dt=1, d_particle=.5,
                                  wakeDeficitModel=PyWakeDeficitGenerator(deficitModel=BastankhahGaussianDeficit()),
                                  site='uniform')
    fs.windTurbines.yaw = 20, -20
    fs.windTurbines.tilt = 6, -6
    fs.run(65)
    x, y, z = fs.particle_positions_xip
    npt.assert_array_almost_equal(y[0], -y[1] + 200)
    npt.assert_array_almost_equal(-y[0], [-0., 2.74, 12.31, 21.85, 30.15, 36.94, 42.53, 47.19, 51.12, 54.47], 2)
    npt.assert_array_almost_equal(z[0] - 70, 70 - z[1])
    npt.assert_array_almost_equal(z[0], [70.0, 70.84, 73.76, 76.68, 79.22, 81.29, 83.0, 84.42, 85.62, 86.65], 2)

    if 0:
        print(np.round(y[0], 2).tolist())
        print(np.round(z[0], 2).tolist())
        plt.plot(x.T, y.T)
        plt.plot(x.T, z.T)

        plt.show()
        fs.visualize(100, dt=1,  # xlim=[0, 100], ylim=[-100, 100],
                     view=XYView(z=70, x=np.linspace(-50, 800, 100), y=np.linspace(-100, 300)))


def test_deflection_ainslie_deficit():
    try:
        import jDWM
        from dynamiks.dwm.particle_deficit_profiles.ainslie import jDWMAinslieGenerator
    except ModuleNotFoundError:
        pytest.xfail('jDWM not installed')

    fs = DefaultDWMFlowSimulation(x=[0, 0], y=[0, 200], particleMotionModel=HillVortexParticleMotion(CutOffFrqLarsen2008),
                                  dt=1, d_particle=.5,
                                  wakeDeficitModel=jDWMAinslieGenerator(),
                                  site='uniform')
    fs.windTurbines.yaw = 20, -20
    fs.windTurbines.tilt = 6, -6
    fs.run(55)
    x, y, z = fs.particle_positions_xip
    npt.assert_array_almost_equal(y[0], -y[1] + 200)
    npt.assert_array_almost_equal(-y[0], [-0., 0.86, 6.05, 11.21, 16.27, 21.18, 25.99, 30.75, 35.41, 39.89], 2)
    npt.assert_array_almost_equal(z[0] - 70, 70 - z[1])
    npt.assert_array_almost_equal(z[0], [70., 70.26, 71.85, 73.42, 74.97, 76.47, 77.94, 79.4, 80.82, 82.19], 2)

    if 0:
        print(np.round(y[0], 2).tolist())
        print(np.round(z[0], 2).tolist())
        plt.plot(x.T, y.T)
        plt.plot(x.T, z.T)

        plt.show()
        fs.visualize(100, dt=1,  # xlim=[0, 100], ylim=[-100, 100],
                     view=XYView(z=70, x=np.linspace(-50, 800, 100), y=np.linspace(-100, 300)))
