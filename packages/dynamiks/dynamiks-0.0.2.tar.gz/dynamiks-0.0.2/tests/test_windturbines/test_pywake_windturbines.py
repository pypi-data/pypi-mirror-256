from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines, ParallelPyWakeWindTurbines
from py_wake.examples.data.hornsrev1 import V80
from dynamiks.utils.test_utils import npt, DefaultDWMFlowSimulation
from py_wake.wind_turbines._wind_turbines import WindTurbines
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
import matplotlib.pyplot as plt
from dynamiks.views import XYView
import numpy as np


def test_windturbines():
    wt_lst = WindTurbines.from_WindTurbine_lst([V80(), GenericWindTurbine(name='G100', diameter=100,
                                                                          hub_height=80, power_norm=2300)])
    wt = PyWakeWindTurbines(x=[50, 500, 1000], y=[100, 0, -100],
                            windTurbine=wt_lst, types=[0, 1, 0])
    npt.assert_array_equal(wt.rotor_position, [[50, 500, 1000],
                                               [100, 0, -100],
                                               [70, 80, 70]])
    npt.assert_array_equal(wt[0].rotor_position, [50, 100, 70])
    assert wt[0].inductionModel.__class__.__name__ == 'InductionMatch'

    npt.assert_array_equal(wt.diameter(), [80, 100, 80])
    assert wt[1].diameter() == 100
    npt.assert_array_equal(wt.hub_height(), [70, 80, 70])
    assert wt[2].hub_height() == 70
    DefaultDWMFlowSimulation(windTurbines=wt)
    r = np.array([0, .25, .5, .75, 1])
    assert wt.axisymetric_induction(r).shape == (5, 3)
    assert wt[0].axisymetric_induction(r).shape == (5, 1)


def test_yaw_tilt():
    wt = PyWakeWindTurbines(x=[50, 500, 1000], y=[100, 0, -100],
                            windTurbine=V80())
    wt.yaw = [10, 20, 30]
    wt.tilt = [1, 2, 3]
    npt.assert_array_equal(wt.yaw_tilt(), [[10., 20., 30.], [1., 2., 3.]])
    npt.assert_array_equal(wt[0].yaw_tilt(), [[10.], [1.]])
    npt.assert_array_equal(wt[1:].yaw_tilt(), [[20., 30.], [2., 3.]])


def get_process_id(self):
    import os
    return os.getpid()


def get_var(self, name):
    return getattr(self, name)


def test_parallel_windturbines():
    wt_lst = WindTurbines.from_WindTurbine_lst([V80(), GenericWindTurbine(name='G100', diameter=100,
                                                                          hub_height=80, power_norm=2300)])
    with ParallelPyWakeWindTurbines(x=[50, 500, 1000], y=[100, 0, -100],
                                    windTurbine=wt_lst, types=[0, 1, 0]) as wt:
        npt.assert_array_equal(wt.rotor_position, [[50, 500, 1000],
                                                   [100, 0, -100],
                                                   [70, 80, 70]])
        npt.assert_array_equal(wt[0].rotor_position, [50, 100, 70])

        npt.assert_array_equal(wt.diameter(), [80, 100, 80])
        assert wt[1].diameter() == 100
        npt.assert_array_equal(wt.hub_height(), [70, 80, 70])
        assert wt[2].hub_height() == 70

        dist_wt = wt.dist_wt
        dist_wt.get_process_id = get_process_id
        dist_wt.test = [f"hej{i}" for i in range(3)]
        dist_wt.get_var = get_var
        assert len(np.unique(dist_wt.get_process_id())) == 3
        assert isinstance(dist_wt[0].get_process_id()[0], int)
        assert dist_wt[0].test[0] == 'hej0'
        npt.assert_array_equal(dist_wt.get_var('test'), ['hej0', 'hej1', 'hej2'])
