from abc import ABC, abstractmethod
import numpy as np
from numpy import newaxis as na


class ParticleDeficitGenerator(ABC):
    @abstractmethod
    def new_particle_deficit(self, initial_position, u0, u_eff):
        ""


class ParticleDeficitProfile(ABC):

    def __init__(self, generator, initial_position, u_scale, ip):
        self.generator = generator
        self._initial_position = initial_position
        self._u_scale = u_scale
        self.ip = ip

    @property
    def initial_position(self):
        return self._initial_position

    def u_scale(self, rel_y=0, rel_z=0):
        return np.atleast_1d(self._u_scale)

    def get_rel_xyz(self, x, rel_y, rel_z):
        rel_x = x - self.initial_position[0]
        shape = [np.shape(np.atleast_1d(v)) for v in [rel_y, rel_z]][isinstance(rel_y, (int, float))]
        return [(np.zeros(shape) + xyz) for xyz in [rel_x, rel_y, rel_z]]

    def get_profile_norm(self, x, rel_y, rel_z):
        if self.initial_position is None:
            return np.zeros_like(rel_y)
        xyz = self.get_rel_xyz(x, rel_y, rel_z)
        return self._get_profile_norm(*xyz)

    def get_profile(self, x, rel_y, rel_z):
        return self.get_profile_norm(x, rel_y, rel_z) * self.u_scale(rel_y, rel_z)

    def get_profile_norm_gradient(self, x, rel_y, rel_z):
        if self.initial_position is None:
            return np.zeros_like(rel_y)
        xyz = self.get_rel_xyz(x, rel_y, rel_z)
        return self._get_profile_norm_gradient(*xyz)

    @abstractmethod
    def _get_profile_norm(self, rel_x, rel_y, rel_z):
        ""

    @abstractmethod
    def deficit_norm_magnitude(self, rel_x):
        ""

    @abstractmethod
    def _get_profile_norm_gradient(self, rel_x, rel_y, rel_z):
        ""


class ParticleNoWakeProfile(ParticleDeficitProfile):
    def __init__(self, generator, ip):
        ParticleDeficitProfile.__init__(self, generator, initial_position=None, u_scale=0, ip=ip)

    def _get_profile_norm(self, rel_x, rel_y, rel_z):
        "return np.zeros_like(rel_y)"

    def _get_profile_norm_gradient(self, rel_x, rel_y, rel_z):
        "return np.zeros_like(rel_y)"

    def deficit_norm_magnitude(self, rel_x):
        "return np.zeros_like(rel_x)"
