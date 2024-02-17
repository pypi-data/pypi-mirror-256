from dynamiks.dwm.particle_deficit_profiles.particle_deficit_profile import ParticleDeficitGenerator,\
    ParticleDeficitProfile
from py_wake import np
from py_wake.utils.model_utils import check_model
from numpy import newaxis as na
from py_wake.utils.gradients import autograd


class PyWakeDeficitGenerator(ParticleDeficitGenerator):
    def __init__(self, deficitModel, scale_with_freestream=False):
        self.scale_with_freestream = scale_with_freestream
        from py_wake.deficit_models.deficit_model import DeficitModel
        check_model(deficitModel, DeficitModel, arg_name='wake_deficitModel')
        self.deficitModel = deficitModel

    def get_kwargs_func(self):
        def get_kwargs(windTurbine):
            u_freestream = windTurbine.rotor_avg_windspeed(include_wakes=False)[0, 0]  # free stream ws
            if self.scale_with_freestream:
                u_scale = u_freestream
                ws = None
            else:
                u_scale = windTurbine.rotor_avg_windspeed(include_wakes=True)[0, 0]  # waked ws
                ws = u_scale

            return {'D_src': windTurbine.diameter(),
                    'TI': windTurbine.rotor_avg_ti(),
                    'h': windTurbine.hub_height(),
                    'CT': windTurbine.ct(ws=ws),
                    'u_freestream': u_freestream,
                    'u_scale': u_scale}
        return get_kwargs

    def new_particle_deficit(self, particle_position, ip, u_freestream, u_scale, D_src, TI, h, CT):

        kwargs = dict(D_src_il=np.reshape(D_src, (1, 1)),
                      WS_ilk=np.reshape(u_freestream / u_scale, (1, 1, 1)),
                      WS_eff_ilk=np.reshape(1, (1, 1, 1)),
                      ct_ilk=np.reshape(CT, (1, 1, 1)),
                      TI_ilk=np.reshape(TI, (1, 1, 1)),
                      TI_eff_ilk=np.reshape(TI, (1, 1, 1)),
                      h_ilk=np.reshape(h, (1, 1, 1)),
                      )
        return PyWakeDeficitProfile(particle_position=particle_position, generator=self,
                                    u_scale=u_scale, ip=ip, kwargs=kwargs)


class PyWakeDeficitProfile(ParticleDeficitProfile):
    def __init__(self, particle_position, generator, kwargs, u_scale, ip):
        ParticleDeficitProfile.__init__(self, generator, particle_position, u_scale, ip)
        self.kwargs = kwargs
        self.kwargs_generator_keys = (self.generator.deficitModel.args4deficit -
                                      {'dw_ijlk', 'hcw_ijlk', 'z_ijlk', 'dh_ijlk', 'cw_ijlk'} - set(self.kwargs.keys()))

    def _get_profile_norm(self, rel_x, rel_y, rel_z):

        kwargs = {'dw_ijlk': rel_x[na, :, na, na],
                  'hcw_ijlk': rel_y[na, :, na, na],
                  'z_ijlk': rel_z[na, :, na, na] + self.kwargs['h_ilk'][:, na],
                  'dh_ijlk': rel_z[na, :, na, na],
                  'cw_ijlk': np.sqrt(rel_z**2 + rel_y**2)[na, :, na, na],
                  ** self.kwargs}
        kwargs_generator = {
            'z_ijlk': lambda: np.reshape(rel_z, (1, len(rel_z), 1, 1)) + kwargs['h_ilk'][:, na],
            'cw_ijlk': lambda: np.reshape(np.sqrt(rel_z**2 + rel_y**2), (1, len(rel_z), 1, 1)),
            'wake_radius_ijl': lambda: self.generator.deficitModel.wake_radius(**kwargs)[:, :, :, 0],
            'wake_radius_ijlk': lambda: self.generator.deficitModel.wake_radius(**kwargs)
        }

        kwargs.update({k: kwargs_generator[k]() for k in self.kwargs_generator_keys})

        return self.generator.deficitModel.calc_deficit(**kwargs).reshape(rel_x.shape)

    def _get_profile_norm_gradient(self, rel_x, rel_y, rel_z):
        dx, dy = autograd(self._get_profile_norm, vector_interdependence=False, argnum=[1, 2])(rel_x, rel_y, rel_z)
        return np.sqrt(dx**2 + dy**2)

    def deficit_norm_magnitude(self, rel_x):
        return self._get_profile_norm(np.atleast_1d(rel_x), np.array(
            [0]), np.array([0])) * self.u_scale(rel_y=0, rel_z=0)
