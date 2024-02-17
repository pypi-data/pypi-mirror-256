import pytest

from dynamiks.sites._site import TurbulenceFieldSite, Site
from dynamiks.sites.turbulence_fields import RandomTurbulence, MannTurbulenceField
from dynamiks.utils.test_utils import npt, tfp, DefaultDWMFlowSimulation
from dynamiks.views import XYView, YZView, Grid3D, Points, XZView, ZView
from dynamiks.visualizers.flow_visualizers import Flow2DVisualizer
import matplotlib.pyplot as plt
import numpy as np
from py_wake.site.shear import PowerShear, LogShear


def test_site():
    ti = 0.08
    site = TurbulenceFieldSite(ws=10, ti=ti, turbulenceField=RandomTurbulence(ws=10, ti=ti))
    uvw = site.get_windspeed(Points([0, 0, 0, 0], [0, 0, 0, 0], [0, 10, 20, 30]))

    npt.assert_array_almost_equal(uvw, [[8.86094, 11.010983, 9.303471, 9.792661],
                                        [-0.04822, -0.474166, -0.875387, 0.415291],
                                        [0.144423, -0.781145, 0.938964, 0.387399]])
    x = np.zeros(10000)
    uvw = site.get_windspeed(Points(x, x, x))
    npt.assert_array_almost_equal(np.mean(uvw, 1), [10, 0, 0], 2)
    npt.assert_array_almost_equal(np.std(uvw, 1), [.8, .64, .4], 2)
    with pytest.raises(AssertionError):
        site.get_windspeed([0, 0, 70])


def test_turbulenceFieldSite():
    ws = 8
    tf = MannTurbulenceField.from_netcdf(tfp + 'mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_256x8x8_1.000x1.00x1.00_s0001.nc',
                                         offset=[0, 0, 0])
    tf.transport_speed = 8
    site = TurbulenceFieldSite(ws=ws, ti=0.1, turbulenceField=tf)

    time = -np.arange(0, 25, .1)
    u = np.array([site.get_windspeed(Points(0, 5, 3.5), t)[0] for t in time]).squeeze()

    x = -time * ws
    u_ref = tf.to_xarray().sel(uvw='u').interp(x=x, y=5, z=3.5) + ws
    if 0:
        plt.plot(time, u)
        plt.plot(time, u_ref, ':')
        plt.show()
    npt.assert_array_almost_equal(u, u_ref)
    da = tf.to_xarray()
    u, v, w = site.get_windspeed(YZView(x=0, y=da.y.values, z=da.z.values, adaptive=False))
    npt.assert_array_almost_equal(da.sel(x=0, uvw='u').values + ws, u.squeeze())
    npt.assert_array_almost_equal(da.sel(x=0, uvw='v').values, v.squeeze())
    npt.assert_array_almost_equal(da.sel(x=0, uvw='w').values, w.squeeze())

    u, v, w = site.get_windspeed(YZView(x=0, adaptive=True))
    npt.assert_array_almost_equal(da.sel(x=0, uvw='u').values + ws, u.squeeze())
    npt.assert_array_almost_equal(da.sel(x=0, uvw='v').values, v.squeeze())
    npt.assert_array_almost_equal(da.sel(x=0, uvw='w').values, w.squeeze())


def test_adaptive_incompatibility():
    fs = DefaultDWMFlowSimulation(site='random')

    with pytest.raises(TypeError, match='Grid undefined. Please specify the grid explicitly when instantiating XYView'):
        Flow2DVisualizer(view=XYView(z=70))(fs)

    with pytest.raises(TypeError, match='Grid undefined. Please specify the grid explicitly when instantiating XYView or set adaptive to True'):
        Flow2DVisualizer(view=XYView(z=70, adaptive=False))(fs)

    fs.site.turbulenceField.x = np.arange(10)
    with pytest.raises(TypeError, match='Grid undefined. Please specify the grid explicitly or set adaptive to True when instantiating XYView'):
        Flow2DVisualizer(view=XYView(z=70))(fs)

    fs.site.turbulenceField.y = np.arange(10)
    fs.site.turbulenceField.z = np.arange(10)
    with pytest.raises(TypeError, match='Grid undefined. Please specify the grid explicitly when instantiating XYView or set adaptive to True'):
        Flow2DVisualizer(view=XYView(z=70, adaptive=False))(fs)


@pytest.mark.parametrize('shear_cls,f', [  # (PowerShear, lambda z, U:(z / 100)**0.1 * U),
    (LogShear, lambda z, U: np.log(z / .03) / np.log(100 / .03) * U)
])
def test_shear(shear_cls, f):
    U = 10

    mannturbfield = MannTurbulenceField.from_netcdf(
        tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_3.200x3.20x3.20_s0001.nc",
        offset=(-2500, -100, 20))
    mannturbfield.scale_TI(ti=0, U=U)
    for turbfield in [mannturbfield, RandomTurbulence(ti=0, ws=10)]:
        site = TurbulenceFieldSite(ws=U, ti=0.1, turbulenceField=turbfield, shear=shear_cls())
        if hasattr(turbfield, 'get_axes'):
            z = turbfield.get_axes(0)[2]
        else:
            z = np.linspace(0, 100)[1:]
        for grid in [ZView(0, 0, z, adaptive=False),
                     Points(x=z * 0, y=z * 0, z=z),
                     Grid3D(slice(1), slice(1), slice(None), axes=[[0], [0], z])]:
            uvw = site.get_windspeed(grid)
            if 0:
                plt.plot(uvw[0], z)
                plt.show()
            npt.assert_array_almost_equal(uvw[0].squeeze(), f(z, U))
