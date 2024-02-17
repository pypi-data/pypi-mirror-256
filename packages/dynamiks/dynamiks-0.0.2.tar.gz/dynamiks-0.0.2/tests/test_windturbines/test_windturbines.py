from h2lib_tests import tfp as h2_tfp
import pytest

from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines
from py_wake.examples.data.hornsrev1 import V80
from py_wake.wind_turbines._wind_turbines import WindTurbines
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import MannTurbulenceField
from dynamiks.utils.test_utils import tfp, DefaultDWMFlowSimulation
from dynamiks.wind_turbines.hawc2_windturbine import HAWC2WindTurbines, HAWC2FreeWindWindTurbines,\
    HAWC2FreeWindWindTurbinesDummy

import numpy as np


def get_site():
    ws = 10
    ti = 0.1
    turbfield = MannTurbulenceField.from_netcdf(
        tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_3.200x3.20x3.20_s0001.nc",
        offset=(-2500, -100, 20))
    turbfield.scale_TI(ti=ti, U=ws)
    site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)
    return site


fn = [h2_tfp + 'DTU_10_MW/htc/DTU_10MW_RWT.htc']
x, y = [50, 500, 1000], [100, 0, -100]


@pytest.mark.parametrize('windTurbines', [
    lambda: PyWakeWindTurbines(x=x, y=y,
                               windTurbine=WindTurbines.from_WindTurbine_lst([
                                   V80(),
                                   GenericWindTurbine(name='G100', diameter=100, hub_height=80, power_norm=2300)])),
    lambda:HAWC2FreeWindWindTurbines(x=x, y=y, htc_filename_lst=fn, types=[0], site=get_site(),
                                     windfield_update_interval=5, suppress_output=True),
    lambda: HAWC2FreeWindWindTurbinesDummy(x=x, y=y, htc_filename_lst=fn, types=[0], site=get_site(),
                                           windfield_update_interval=5, suppress_output=True)])
def test_dims(windTurbines):
    windTurbines = windTurbines()
    fs = DefaultDWMFlowSimulation(windTurbines=windTurbines)
    for _ in range(2):
        for N, wts in [(3, windTurbines), (1, windTurbines[:1]), (1, windTurbines[0])]:
            assert wts.diameter().shape == (N,)
            assert wts.hub_height().shape == (N,)
            assert wts.yaw_tilt().shape == (2, N)
            assert wts.ct().shape == (N,)
            assert wts.power().shape == (N,)
            assert wts.rotor_avg_induction().shape == (N,)
            assert np.shape(wts.axisymetric_induction(r=np.linspace(0, 1, 5))) == (5, N)
        fs.step()
