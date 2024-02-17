import numpy as np
from hipersim._hipersim import MannTurbulenceField
from numpy import newaxis as na
from hipersim.turbgen.spectral_tensor import MannTurbulenceInput
import os
from dynamiks.views import Grid3D, Grid


class AddedTurbulenceModel():
    ""


class IsotropicMannTurbulence(AddedTurbulenceModel):

    def __init__(self, mannTurbulenceField, km1=0.6, km2=0.35):
        self.mannTurbulenceField = mannTurbulenceField
        self.km1 = km1
        self.km2 = km2

    def initialize(self, flowSimulation):
        self.transport_speed = flowSimulation.site.ws
        self.wt_diameters = flowSimulation.windTurbines.diameter()

    def to_netcdf(self, folder='', filename=None):
        self.mannTurbulenceField.to_netcdf(folder, filename)

    @staticmethod
    def from_netcdf(filename, km1=0.6, km2=0.35):
        mtf = MannTurbulenceField.from_netcdf(filename)
        return IsotropicMannTurbulence(mannTurbulenceField=mtf, km1=km1, km2=km2)

    @staticmethod
    def generate(D, Nxyz=(128, 128, 128), seed=1, km1=0.6, km2=0.35, cache_spectra_tensor=False):
        dxyz = np.array([2.5, 1, 1]) * D / Nxyz
        mtf = MannTurbulenceField.generate(
            alphaepsilon=1, L=D / 16., Gamma=0, Nxyz=Nxyz, dxyz=dxyz, seed=seed,
            HighFreqComp=False, double_xyz=(0, 0, 0), cache_spectral_tensor=cache_spectra_tensor)
        return IsotropicMannTurbulence(mannTurbulenceField=mtf, km1=km1, km2=km2)

    def scale(self, U, target_std=1):
        # to scale the turbulence, we need to calculate the variance of the spectra
        # from a lower cut-off frequency (which corresponds to the Lx / transport speed) and up
        Lx = (self.mannTurbulenceField.Nxyz[0] - 1) * self.mannTurbulenceField.dxyz[0]
        T = Lx / U
        self.mannTurbulenceField.scale_TI(ti=target_std, U=1, T=T)  # U=1 as ti=target_std for U=1

    def __call__(self, xyz, time, wt_idx, rotor_position, deficit_norm, deficit_norm_gradient):
        if isinstance(xyz, Grid):
            xyz = np.meshgrid(xyz.x, xyz.y, xyz.z, indexing='ij')

        added_turb_weight = self.km1 * (np.abs(deficit_norm) + self.km2 * np.abs(deficit_norm_gradient))
        x, y, z = [v - rp for v, rp in zip(xyz, rotor_position)]
        x = x - self.transport_speed * time
        add_turb_uvw = np.moveaxis(self.mannTurbulenceField(x, y, z), -1, 0).reshape((3,) + np.shape(deficit_norm))
        return add_turb_uvw * added_turb_weight[na]


class AutoScalingIsotropicMannTurbulence(IsotropicMannTurbulence):
    _flowSimulation = None

    def __init__(self, cache_field=True, seed=1):
        self.cache_field = cache_field
        IsotropicMannTurbulence.__init__(self, mannTurbulenceField=None)
        self.seed = seed

    def initialize(self, flowSimulation):
        IsotropicMannTurbulence.initialize(self, flowSimulation)
        Nxyz = [128] * 3
        dxyz = np.array([2.5, 1, 1]) * np.max(self.wt_diameters) / Nxyz
        self.generate(dxyz, Nxyz)

    def generate(self, dxyz, Nxyz=(128, 128, 128)):
        D = np.max(self.wt_diameters)
        self.Nxyz = Nxyz
        kwargs = dict(alphaepsilon=1, L=D / 16., Gamma=0, Nxyz=Nxyz, dxyz=dxyz, seed=self.seed,
                      HighFreqComp=0, double_xyz=(0, 0, 0))
        fn = MannTurbulenceInput(**kwargs, generator='Hipersim').name + ".nc"
        if self.cache_field:
            if os.path.isfile(fn):
                self.mannTurbulenceField = MannTurbulenceField.from_netcdf(fn)
            else:
                self.mannTurbulenceField = MannTurbulenceField.generate(**kwargs)
                self.to_netcdf()
        else:
            self.mannTurbulenceField = MannTurbulenceField.generate(**kwargs)
        self.scale(U=self.transport_speed)


class SynchronizedAutoScalingIsotropicMannTurbulence(AutoScalingIsotropicMannTurbulence):

    def initialize(self, flowSimulation):
        IsotropicMannTurbulence.initialize(self, flowSimulation)
        self.generate(dxyz=flowSimulation.site.turbulenceField.dxyz)
        np.random.seed(self.seed)
        self.ioffsets = np.random.randint(0, 128, (3, flowSimulation.n_wt))
        self.offsets = self.ioffsets * np.asarray(self.mannTurbulenceField.dxyz)[:, na]
        self.main_turublenceField_Nxyz = flowSimulation.site.turbulenceField.Nxyz

    def __call__(self, xyz, time, wt_idx, rotor_position, deficit_norm, deficit_norm_gradient):
        if isinstance(xyz, Grid3D):
            added_turb_weight = self.km1 * (np.abs(deficit_norm) + self.km2 * np.abs(deficit_norm_gradient))
            grid = xyz

            def get_idx(s, N_big, N_micro, offset):
                if isinstance(s, slice):
                    s = np.arange(N_big)[s]
                return ((s + offset) % N_micro)
            idx = [get_idx(s, N, 128, o)
                   for s, N, o in zip(grid.slices, self.main_turublenceField_Nxyz, self.ioffsets[:, wt_idx])]
            add_turb_uvw = self.mannTurbulenceField.uvw
            add_turb_uvw = add_turb_uvw[np.ix_([0, 1, 2], idx[0], idx[1], idx[2])]
            return add_turb_uvw * added_turb_weight[na]
        else:
            return AutoScalingIsotropicMannTurbulence.__call__(self, xyz, time, wt_idx, -self.offsets[:, wt_idx],
                                                               deficit_norm, deficit_norm_gradient)
