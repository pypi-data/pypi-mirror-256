import matplotlib.pyplot as plt
import numpy as np
from dynamiks.sites.turbulence_fields import RandomTurbulence, MannTurbulenceField
import pytest
from numpy import newaxis as na
from dynamiks.utils.test_utils import npt, tfp, DefaultDWMFlowSimulation
import os
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.views import Grid3D, Points
from py_wake.utils.grid_interpolator import GridInterpolator


def test_random_turbulence_field():
    # Check mean and std of mann
    turb = RandomTurbulence(ws=10, ti=.08)
    uvw = turb([0, 0, 0, 0], y=[0, 0, 0, 0], z=[0, 10, 20, 30])

    npt.assert_array_almost_equal(uvw, [[-1.13906, 1.010983, -0.696529, -0.207339],
                                        [-0.04822, -0.474166, -0.875387, 0.415291],
                                        [0.144423, -0.781145, 0.938964, 0.387399]])
    x = np.zeros(10000)
    uvw = turb(x, x, x)
    npt.assert_array_almost_equal(np.mean(uvw, 1), [0, 0, 0], 2)
    npt.assert_array_almost_equal(np.std(uvw, 1), [.8, .64, .4], 2)


def test_turbulence_field_generate():

    tf = MannTurbulenceField.generate(offset=(0, 0, 0), L=29.4, Nxyz=(256, 8, 8))

    # save for reference test
    # tf.save(tfp + 'mann_turb')

    tf_ref = MannTurbulenceField.from_netcdf(
        tfp + 'mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_256x8x8_1.000x1.00x1.00_s0001.nc',
        offset=(0, 0, 0))
    x = np.linspace(tf.x[0], tf.x[-1])

    if 0:
        u = tf(x=x, y=np.full_like(x, 5), z=np.full_like(x, 3.5))[0]
        plt.plot(x, u, '.-')
        plt.plot(x, tf_ref(x=x, y=np.full_like(x, 5), z=np.full_like(x, 3.5))[0])
        tf_ref.dataArray.interp(x=x, y=5, z=3.5).sel(uvw='u').squeeze().plot()
        plt.show()

    npt.assert_array_almost_equal(tf(x=x, y=np.full_like(x, 5), z=np.full_like(x, 3.5), time=0),
                                  tf_ref.to_xarray().interp(x=x, y=5, z=3.5))

    if os.path.isfile(tfp + 'tmp.nc'):
        os.remove(tfp + 'tmp.nc')
    tf.to_netcdf(folder=tfp, filename='tmp.nc')
    tf_saved = MannTurbulenceField.from_netcdf(tfp + 'tmp.nc', offset=(0, 0, 0))
    assert tf.to_xarray().equals(tf_saved.to_xarray())


def get_linear_turbulence(Nxyz, dxyz):
    Nx, Ny, Nz = Nxyz
    u = np.arange(Nx)[:, na, na] * np.ones((Nxyz))
    v = np.arange(Ny)[na, :, na] * np.ones((Nxyz))
    w = np.arange(Nz)[na, na, :] * np.ones((Nxyz))

    return MannTurbulenceField(offset=[0, 0, 0], uvw=np.array([u, v, w]), Nxyz=Nxyz, dxyz=dxyz,
                               alphaepsilon=1, L=1, Gamma=1, seed=-1)


@pytest.mark.parametrize('dxyz', [(1, 1, 1), (2, 4, 6)])
def test_interpolation(dxyz):
    dx, dy, dz = dxyz
    turb_field = get_linear_turbulence((16, 8, 4), dxyz)

    x, y, z = np.array([[3.1, 4.2, 2.3],
                        [4.4, 5.5, 2.6]]).T
    npt.assert_array_almost_equal(turb_field(x * dx, y * dy, z * dz, time=0), [x, y, z])


def test_from_hawc2():
    dx, dy, dz = dxyz = (2, 4, 6)
    ref = get_linear_turbulence((16, 8, 4), dxyz)
    ref.to_hawc2(tfp, 'tmp')
    filenames = [os.path.join(tfp + f"tmp{uvw}.turb") for uvw in 'uvw']
    turb_field = MannTurbulenceField.from_hawc2(filenames, offset=[0, 0, 0], Nxyz=ref.Nxyz, dxyz=dxyz,
                                                alphaepsilon=1, L=1, Gamma=1, seed=-1)
    attrs = [k for k in dir(turb_field)
             if isinstance(getattr(turb_field, k), (int, float, np.integer, tuple, str, list, np.ndarray))]
    for k in attrs:
        npt.assert_array_equal(getattr(turb_field, k), getattr(ref, k))


def test_get_slices():
    fs = DefaultDWMFlowSimulation()
    site = fs.site
    tf = site.turbulenceField

    y_slice = tf.get_slice(0, 1, 0)
    z_slice = tf.get_slice(70, 2, 0)
    for t in [0, 30]:
        site.time = t
        for x in [-3000, 0, 1000]:
            ref = site.get_windspeed(Points(x, 0, 70))
            grid = Grid3D(
                tf.get_slice(x, 0, site.time), y_slice, z_slice,
                axes=tf.get_axes(site.time))
            uvw_g = site.get_windspeed(grid)

            uvw = GridInterpolator(list(grid), np.moveaxis(uvw_g, 0, -1))((x, 0, 70)).T
            npt.assert_array_almost_equal(ref, uvw)
