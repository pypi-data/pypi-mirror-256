import pytest

from dynamiks.dwm.flow_simulation import DWMFlowSimulation
from dynamiks.dwm.particle_deficit_profiles.pywake_deficit_wrapper import PyWakeDeficitGenerator
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import RandomTurbulence
from dynamiks.utils.data_dumper import DataDumper
from dynamiks.utils.test_utils import npt
from dynamiks.views import XYView, XView
from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines
import matplotlib.pyplot as plt
import numpy as np
from py_wake.deficit_models.noj import NOJDeficit
from py_wake.deficit_models.utils import ct2a_mom1d
from py_wake.superposition_models import LinearSum, SquaredSum, MaxSum
from py_wake.tests.test_deficit_models.test_noj import NibeA0
from dynamiks.dwm.particle_motion_models import ParticleMotionModel
d02 = 8.1 - 5.7
d12 = 8.1 - 4.90473373


@pytest.mark.parametrize('superpositionModel,res,u_ref', [
    (LinearSum(), 8.1 - (d02 + d12), [2.7, 3.2, 3.64, 4.02, -1.05, -0.26, 0.44, 1.05]),
    (SquaredSum(), 8.1 - np.hypot(d02, d12), [2.7, 3.2, 3.64, 4.02, 1.53, 2.1, 2.61, 3.05]),
    (MaxSum(), 8.1 - d12, [2.7, 3.2, 3.64, 4.02, 2.7, 3.2, 3.64, 4.02])
])
def test_superposition(superpositionModel, res, u_ref):
    ti = 0
    ws = 8.1
    site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=RandomTurbulence(ti=ti, ws=ws))

    windTurbines = PyWakeWindTurbines(x=[0, 40, 100], y=[0, 0, 0], windTurbine=NibeA0(), types=[0, 0, 1])
    wakeDeficitModel = PyWakeDeficitGenerator(deficitModel=NOJDeficit(ct2a=ct2a_mom1d, rotorAvgModel=None),
                                              scale_with_freestream=True)
    data_dumper = DataDumper(lambda fs: fs.get_windspeed([100, 0, 50], include_wakes=True)[0])

    step_handlers = [data_dumper]

    fs = DWMFlowSimulation(site, windTurbines, dt=.1, step_handlers=step_handlers,
                           n_particles=30, d_particle=.1, wakeDeficitModel=wakeDeficitModel,
                           particleMotionModel=ParticleMotionModel(cut_off_frequency=0.1),
                           superpositionModel=superpositionModel, addedTurbulenceModel=None)

    if 0:
        fs.visualize(15, view=XYView(z=50, x=np.linspace(-50, 150, 100), y=np.linspace(-50, 50, 100), adaptive=False),
                     particleProfileVisualizer=False)
        plt.figure()
        data_dumper.to_xarray().plot()
        plt.show()
    else:
        fs.run(15)

    npt.assert_allclose(data_dumper.data[-1], res, rtol=0.001)
    u = fs.get_windspeed(XView(x=np.arange(0, 80, 10), y=0, z=50, adaptive=False),
                         include_wakes=True)[0].squeeze()
    # print(np.round(u,2).tolist())
    npt.assert_array_almost_equal(u, u_ref, 2)
