import pytest
from tqdm import tqdm

from dynamiks.dwm.flow_simulation import DWMFlowSimulation
from dynamiks.dwm.particle_deficit_profiles.pywake_deficit_wrapper import PyWakeDeficitGenerator
from dynamiks.dwm.particle_motion_models import ParticleMotionModel
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import MannTurbulenceField
from dynamiks.utils.test_utils import npt, tfp, DefaultDWMFlowSimulation
from dynamiks.wind_turbines.hawc2_windturbine import HAWC2WindTurbines, hawc2gl_to_uvw, HAWC2FreeWindWindTurbines,\
    HAWC2FreeWindWindTurbinesDummy
import matplotlib.pyplot as plt
import numpy as np
from py_wake.deficit_models.no_wake import NoWakeDeficit
from tests.test_windturbines.test_pywake_windturbines import get_process_id, get_var


def test_gl2uvw():
    xyz_wt = np.array([[100, -100],
                       [50, 500],
                       [-118, -150.]])

    npt.assert_array_equal(hawc2gl_to_uvw(xyz_wt), [[50., 500.],
                                                    [100., -100.],
                                                    [118., 150.]])

    npt.assert_array_equal(hawc2gl_to_uvw(xyz_wt.T, 1), [[50., 500.],
                                                         [100., -100.],
                                                         [118., 150.]])

    npt.assert_array_equal(hawc2gl_to_uvw([100, 50, -118]), [50, 100, 118])


def test_windturbine():
    from h2lib_tests.test_files import tfp as h2lib_tfp
    htc_filename_lst = [h2lib_tfp + "DTU_10_MW/htc/DTU_10MW_RWT.htc"]
    wt = HAWC2WindTurbines(x=[50], y=[100], htc_filename_lst=htc_filename_lst, types=0, suppress_output=True)
    npt.assert_array_almost_equal(wt.rotor_position.squeeze(), [42.927018, 100, 118.99880577])

    npt.assert_array_almost_equal(wt.diameter() / 2, 88.95765294)
    npt.assert_array_almost_equal(wt.hub_height(), 118.99880577)

    fs = DefaultDWMFlowSimulation(windTurbines=wt, dt=0.01)
    r = np.array([0, .25, .5, .75, 1])
    assert wt[0].axisymetric_induction(r).shape == (5, 1)
    assert wt.axisymetric_induction(r).shape == (5, 1)
    assert wt[:1].axisymetric_induction(r).shape == (5, 1)
    fs.step()
    npt.assert_array_almost_equal(wt.axisymetric_induction([0, .5, 1])[:, 0],
                                  [1.45886460e-01, 6.94619126e-02, 2.09019468e-11], 5)


def test_windturbines():
    from h2lib_tests.test_files import tfp as h2lib_tfp
    htc_filename_lst = [h2lib_tfp + "DTU_10_MW/htc/DTU_10MW_RWT.htc",
                        h2lib_tfp + "IEA-15-240-RWT-Onshore/htc/IEA_15MW_RWT_Onshore.htc"]
    wt = HAWC2WindTurbines(x=[50, 500, 1000], y=[100, 0, -100], htc_filename_lst=htc_filename_lst, types=[0, 1, 0],
                           suppress_output=True)
    npt.assert_array_almost_equal(wt.rotor_position, [[42.927018, 487.9687, 992.927018],
                                                      [100., 0., -100.],
                                                      [118.998806, 150., 118.998806]])
    npt.assert_array_almost_equal(wt[0].rotor_position.squeeze(), [42.927018, 100, 118.99880577])

    npt.assert_array_almost_equal(wt.diameter() / 2, [88.95765294, 120.40297962, 88.95765294])
    npt.assert_array_almost_equal(wt[1].diameter() / 2, 120.40297962)
    npt.assert_array_almost_equal(wt.hub_height(), [118.99880577, 150., 118.99880577])
    npt.assert_array_almost_equal(wt[2].hub_height(), 118.99880577)

    fs = DefaultDWMFlowSimulation(windTurbines=wt, dt=0.01)
    r = np.array([0, .25, .5, .75, 1])
    assert wt[0].axisymetric_induction(r).shape == (5, 1)
    fs.step()
    npt.assert_array_almost_equal(wt[0].axisymetric_induction([0, .5, 1])[:, 0],
                                  [1.45886460e-01, 6.94619126e-02, 2.09019468e-11], 5)

    dist_wt = wt.dist_wt
    dist_wt.get_process_id = get_process_id
    dist_wt.test = [f"hej{i}" for i in range(3)]
    dist_wt.get_var = get_var
    assert len(np.unique(dist_wt.get_process_id())) == 3
    assert isinstance(dist_wt[0].get_process_id()[0], int)
    npt.assert_array_equal(dist_wt.get_var('test'), ['hej0', 'hej1', 'hej2'])


@pytest.mark.parametrize('offset', [-500, -2500, -10000])
def test_set_windfield_1wt(offset):
    from h2lib_tests.test_files import tfp as h2lib_tfp
    ws = 20
    ti = .1
    turbfield = MannTurbulenceField.from_netcdf(
        tfp + "mann_turb/Hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_9.600x9.60x9.60_s0001.nc",
        offset=(offset, -100, 20))
    from numpy import newaxis as na
    turbfield.uvw[0] = np.arange(1024)[:, na, na]
    turbfield.uvw[1] = np.arange(128)[na, :, na]
    turbfield.uvw[2] = np.arange(32)[na, na, :]
    site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)

    wt = HAWC2FreeWindWindTurbines(x=[0], y=[50], htc_filename_lst=[h2lib_tfp + "DTU_10_MW/htc/DTU_10MW_RWT.htc"],
                                   types=[0], site=site, suppress_output=True, windfield_update_interval=0.4)

    fs = DWMFlowSimulation(site, windTurbines=wt, dt=.2,
                           d_particle=2, n_particles=100,
                           wakeDeficitModel=PyWakeDeficitGenerator(deficitModel=NoWakeDeficit()),
                           particleMotionModel=ParticleMotionModel(cut_off_frequency=0.1))

    for _ in range(5):
        fs.step()
        npt.assert_array_almost_equal(fs.get_windspeed([0, 50, 100], include_wakes=False)[:, 0],
                                      wt.h2.get_uvw([0, 0, -100])[0])
        npt.assert_array_almost_equal(fs.get_windspeed([0, 50, 100], include_wakes=False),
                                      wt.get_windspeed(0, 50, 100))

    if offset == -2500:
        r = np.linspace(0, 1, 10)
        a = wt.axisymetric_induction(r)[:, 0]
        ref = [0.11, 0.05, 0.04, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.0]
        if 0:
            plt.plot(r, np.round(a, 2), label='actual')
            plt.plot(r, ref, label='ref')
            plt.legend()
            plt.show()
        # print(np.round(a, 2).tolist())
        npt.assert_array_almost_equal(a, ref, 2)


def test_set_windfield_3wt():
    from h2lib_tests.test_files import tfp as h2lib_tfp
    ws = 20
    ti = .1
    turbfield = MannTurbulenceField.from_netcdf(
        tfp + "mann_turb/Hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_9.600x9.60x9.60_s0001.nc",
        offset=(-2500, -100, 10))
    from numpy import newaxis as na
    turbfield.uvw[0] = np.arange(1024)[:, na, na]
    turbfield.uvw[1] = np.arange(128)[na, :, na]
    turbfield.uvw[2] = np.arange(32)[na, na, :]
    site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)
    htc_filename_lst = [h2lib_tfp + "DTU_10_MW/htc/DTU_10MW_RWT.htc",
                        h2lib_tfp + "IEA-15-240-RWT-Onshore/htc/IEA_15MW_RWT_Onshore_simple.htc"]
    wt = HAWC2FreeWindWindTurbines(x=[-2500, 500, 7330.4], y=[50, 100, 150], htc_filename_lst=htc_filename_lst,
                                   types=[0, 1, 0], site=site, suppress_output=True, windfield_update_interval=0.4)

    fs = DWMFlowSimulation(site, windTurbines=wt, dt=.2, d_particle=2, n_particles=100,
                           wakeDeficitModel=PyWakeDeficitGenerator(deficitModel=NoWakeDeficit()),
                           particleMotionModel=ParticleMotionModel(cut_off_frequency=0.1))

    for _ in range(5):
        fs.step()
        xyz = wt.rotor_position
        npt.assert_array_almost_equal(fs.get_windspeed(xyz, include_wakes=False),
                                      wt.get_windspeed(*xyz))
    npt.assert_array_almost_equal(wt.yaw_tilt(),
                                  [[-0.000480616303979246, -3.320634660331569e-05, -0.000480616303979246],
                                   [0.086104662375323, 0.09662980122800646, 0.086104662375323]])


def test_HAWC2FreeWindWindTurbinesDummy():
    x, y = [0, 500], [0, 0]
    ws = 10
    ti = 0.1
    turbfield = MannTurbulenceField.from_netcdf(
        tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_3.200x3.20x3.20_s0001.nc",
        offset=(-2500, -100, 20))
    turbfield.scale_TI(ti=ti, U=ws)
    site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)

    from h2lib_tests import tfp as h2_tfp
    fn = [h2_tfp + 'DTU_10_MW/htc/DTU_10MW_RWT.htc']
    windTurbines = HAWC2FreeWindWindTurbinesDummy(x=x, y=y, htc_filename_lst=fn, types=[0], site=site,
                                                  windfield_update_interval=5,
                                                  suppress_output=True)

    fs = DefaultDWMFlowSimulation(x, y, ws=ws, ti=ti, site=site, windTurbines=windTurbines)
    fs.run(1)


#
# def test_dwm_ainslie():
#     from h2lib_tests.test_files import tfp as h2lib_tfp
#     ws = 10
#     ti = .1
#     turbfield = MannTurbulenceField.from_netcdf(
#         tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_9.600x9.60x9.60_s0001.nc",
#         transport_speed=ws, offset=(-2500, -100, 10))
#     from numpy import newaxis as na
#     turbfield.scale_TI(ti=ti, U=ws)
#     site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)
#     htc_filename_lst = [h2lib_tfp + "DTU_10_MW/htc/DTU_10MW_RWT.htc",
#                         h2lib_tfp + "IEA-15-240-RWT-Onshore/htc/IEA_15MW_RWT_Onshore.htc"]
#     wt = HAWC2FreeWindWindTurbines(x=[0, 500, 1000], y=[100, 100, 100], htc_filename_lst=htc_filename_lst,
#                                    types=[0, 1, 0], site=site, suppress_output=True, windfield_update_interval=5)
#
#     if 1:
#         fig = InteractiveFigure()
#
#         axes = np.atleast_1d(fig.subplots(1, figsize=(10, 8))[1])
#         xz_view = XZView(y=100, x=np.arange(-100, 1100))
#         step_handlers = [
#             AxesInitializer(ax=axes[0], axis='scaled', ylabel='y [m]', xlabel='x [m]', xlim=[-100, 1100]),
#             Flow2DVisualizer(view=xz_view, ax=axes[0]),
#             ParticleProfileVisualizer(axes[0], view=xz_view),
#             xz_view.get_plot_windturbines(axes[0]),
#             fig
#         ]
#     else:
#         step_handlers = []
#     fs = DWMFlowSimulation(site, windTurbines=wt,
#                            wakeDeficitModel=jDWMAinslieGenerator(),
#                            d_particle=.2, n_particles=50, dt=1, fc=.1, step_handlers=step_handlers)
#
#     for _ in tqdm(range(3)):
#         fs.step(1)
#
#         print(fs.time, wt.ct())
#         print(wt[0].axisymetric_induction())
if __name__ == '__main__':
    test_HAWC2FreeWindWindTurbinesDummy()
