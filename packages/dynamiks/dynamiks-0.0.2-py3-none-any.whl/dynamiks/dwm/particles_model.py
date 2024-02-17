import warnings

from dynamiks.dwm.particle_deficit_profiles.particle_deficit_profile import ParticleNoWakeProfile,\
    ParticleDeficitProfile
import numpy as np
from py_wake.utils.grid_interpolator import GridInterpolator
import os
from numpy import newaxis as na
from multiclass_interface.multi_object_list import MultiObjectList
from dynamiks.views import Grid, Points, Grid3D
from multiclass_interface.multiprocess_interface import MultiProcessClassInterface
from py_wake.utils.profiling import timeit


class WindTurbinesParticles(MultiObjectList):
    def __init__(self, windTurbines, n_particles, wakeDeficitModel, addedTurbulenceModel):
        R_lst = windTurbines.diameter() / 2
        MultiObjectList.__init__(self, [WindTurbineParticles(n_particles, R, wakeDeficitModel, addedTurbulenceModel, wt_index)
                                        for wt_index, R in enumerate(R_lst)])


def DistributedWindTurbinesParticles(windTurbines, n_particles, wakeDeficitModel, addedTurbulenceModel):
    dist_wt = windTurbines.dist_wt
    R_lst = windTurbines.diameter() / 2
    dist_wt.windTurbineParticles = [WindTurbineParticles(n_particles, R, wakeDeficitModel, addedTurbulenceModel, wt_index)
                                    for wt_index, R in enumerate(R_lst)]

    dist_wt.get_deficit = get_deficit
    dist_wt.reset_particle = reset_particle
    return dist_wt


def get_deficit(self, *args, **kwargs):  # pragma: no cover  # run in separate process
    return self.windTurbineParticles.get_deficit(*args, **kwargs)


def reset_particle(self, *args, **kwargs):  # pragma: no cover  # run in separate process
    return self.windTurbineParticles.reset_particle(*args, **kwargs)


class WindTurbineParticles():
    def __init__(self, n_particles, R, wakeDeficitModel, addedTurbulenceModel, wt_index):
        self.n_particles = n_particles
        self.R = R
        self.wakeDeficitModel = wakeDeficitModel
        self.addedTurbulenceModel = addedTurbulenceModel
        self.particles = np.array([ParticleNoWakeProfile(generator=self, ip=(wt_index, p))
                                  for p in range(self.n_particles)])
        self.iwt = wt_index

    def reset_particle(self, p, particle_positions_x, kwargs):
        self.particles[p] = self.wakeDeficitModel.new_particle_deficit(
            particle_positions_x, ip=(self.iwt, p),
            ** kwargs)

    def get_deficit(self, xyz, particle_positions_xp, mask_p, t, rotor_position):
        if isinstance(xyz, Points):
            x, y, z = [np.atleast_1d(v) for v in xyz]
            YZ = [y, z]
            assert len(np.unique(x)) == 1
            x = np.unique(x)
            s = np.shape(np.atleast_1d(y))
        else:
            s = xyz.shape

            if isinstance(xyz, Grid):
                x, y, z = [np.atleast_1d(v) for v in [xyz.x, xyz.y, xyz.z]]
                YZ = np.meshgrid(y, z, indexing='ij')

        if self.addedTurbulenceModel:
            u_deficit_norm_y = self.get(ParticleDeficitProfile.get_profile_norm, x, *YZ,
                                        particle_positions_xp, mask_p).reshape(s)
            deficit_norm_gradient_y = self.get(ParticleDeficitProfile.get_profile_norm_gradient, x, *YZ,
                                               particle_positions_xp, mask_p).reshape(s)
            deficit_norm_gradient_norm_y = deficit_norm_gradient_y * self.R
            deficit_uy = self.addedTurbulenceModel(
                xyz, t, self.iwt, rotor_position, u_deficit_norm_y, deficit_norm_gradient_norm_y).reshape((3,) + s)
        else:
            deficit_uy = np.zeros((3,) + s)
        deficit_uy[0] += self.get(ParticleDeficitProfile.get_profile, x, *YZ, particle_positions_xp, mask_p).reshape(s)
        return deficit_uy

    def get(self, cls_method, x, y_j, z_j, particle_positions_xp, mask_p):

        x0s, y0s, z0s = particle_positions_xp[:, mask_p]
        grid_pyz = np.array([cls_method(p, x0, y_j - y0, z_j - z0)
                             for p, x0, y0, z0 in zip(self.particles[mask_p], x0s, y0s, z0s)])  # loop over particles
        if len(np.atleast_1d(np.unique(x))) == 1:
            # single x
            x0, x1 = particle_positions_xp[0, mask_p]
            dx = x1 - x0
            with warnings.catch_warnings():
                # warnings.filterwarnings('ignore', r'divide by zero encountered in divide')
                warnings.filterwarnings('ignore', r'invalid value encountered in scalar divide')
                warnings.filterwarnings('ignore', r'invalid value encountered in double_scalars')
                warnings.filterwarnings('ignore', r'invalid value encountered in divide')
                w0 = np.where(dx != 0, ((x1 - x) / dx), 1)
            return grid_pyz[0] * w0 + grid_pyz[1] * (1 - w0)
        else:
            # multiple x
            interp = GridInterpolator([np.r_[x0s.min() - 1e-6, x0s]],
                                      np.concatenate([grid_pyz[:1] * 0, grid_pyz]))
            return interp(np.array([x]).T, bounds='limit')
