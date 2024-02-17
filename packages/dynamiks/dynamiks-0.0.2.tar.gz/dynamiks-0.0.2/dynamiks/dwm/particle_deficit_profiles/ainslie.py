import numpy as np
from dynamiks.dwm.particle_deficit_profiles.particle_deficit_profile import ParticleDeficitGenerator,\
    ParticleDeficitProfile
from jDWM import BoundaryCondition
from jDWM import EddyViscosityModel
from jDWM.Solvers import implicit


class jDWMAinslieGenerator(ParticleDeficitGenerator):
    def __init__(self, boundaryConditionModel_cls=BoundaryCondition.madsen,
                 viscosity_model_cls=EddyViscosityModel.madsen, solver=implicit(),
                 scale_with_freestream=False, r_max=3, n_r=51):
        assert issubclass(viscosity_model_cls, EddyViscosityModel.EddyViscosityModel)
        assert issubclass(boundaryConditionModel_cls, BoundaryCondition.BoundaryCondition)

        self.viscosity_model_cls = viscosity_model_cls
        self.solver = solver
        self.boundaryConditionModel = boundaryConditionModel_cls()
        self.scale_with_freestream = scale_with_freestream
        self.r_max = r_max
        self.n_r = n_r

    def get_kwargs_func(self):
        def kwargs_func(windTurbine):
            u_scale = windTurbine.rotor_avg_windspeed(include_wakes=not self.scale_with_freestream)[0]
            r = np.linspace(0, self.r_max, self.n_r)
            a = windTurbine.axisymetric_induction(r)[:, 0]
            TI = windTurbine.rotor_avg_ti()[0]
            return {'u_scale': u_scale,
                    'a': a,
                    'TI': TI,
                    'D': windTurbine.diameter()}
        return kwargs_func

    def new_particle_deficit(self, particle_position, ip, u_scale, a, TI, D):
        r = np.linspace(0, self.r_max, self.n_r)
        U, V = self.boundaryConditionModel(r, a)
        return AinslieDeficitProfile(generator=self, particle_position=particle_position, ip=ip,
                                     u_scale=u_scale,
                                     diameter=D, r=r, U=U, V=V, TI=TI)


class AinslieDeficitProfile(ParticleDeficitProfile):
    def __init__(self, generator, particle_position, ip, diameter, u_scale, r, U, V, TI, dx=0.1):
        ParticleDeficitProfile.__init__(
            self,
            generator=generator,
            initial_position=particle_position,
            u_scale=u_scale,
            ip=ip)
        self.R = diameter / 2
        self.r = r
        self.dr = r[1] - r[0]
        self.U = U
        self.V = V
        self.dx = dx
        self.evolved_x_R = 0
        self.dUdr = U * 0
        self.viscosity_model = self.generator.viscosity_model_cls(TI=TI)

    def evolve_profile(self, dx):
        self.evolved_x_R += dx
        visc = self.viscosity_model(self.evolved_x_R, self.r, self.U)
        self.U, self.V = self.generator.solver.evolve(self.r, self.U, self.V, visc, dx, self.dr)
        self.dUdr = np.gradient(self.U, self.dr)

    def _get_profile_norm(self, rel_x, rel_y, rel_z):
        rel_x, rel_y, rel_z = [v / self.R for v in [rel_x, rel_y, rel_z]]
        deficit = np.zeros(rel_x.shape)
        for x in np.sort(np.unique(rel_x)):
            m = rel_x == x
            while (self.evolved_x_R + self.dx) < x:
                self.evolve_profile(self.dx)
            if x > self.evolved_x_R:
                self.evolve_profile(x - self.evolved_x_R)

            deficit[m] = np.interp(rel_y[m]**2 + rel_z[m]**2, self.r**2, 1 - self.U)
        return deficit

    def _get_profile_norm_gradient(self, rel_x, rel_y, rel_z):
        rel_x, rel_y, rel_z = [v / self.R for v in [rel_x, rel_y, rel_z]]
        assert len(np.unique(rel_x)) == 1
        assert np.unique(rel_x) == self.evolved_x_R, (self.ip,
                                                      np.unique(rel_x), self.evolved_x_R)  # Call get_profile first
        deficit_gradient_norm = np.interp(rel_y**2 + rel_z**2, self.r**2, self.dUdr)
        return deficit_gradient_norm / self.R

    def deficit_norm_magnitude(self, rel_x):
        if rel_x > self.evolved_x_R * self.R:
            self._get_profile_norm(rel_x, rel_y=0, rel_z=0)
        return self.u_scale(0, 0) * (1 - self.U.min())
