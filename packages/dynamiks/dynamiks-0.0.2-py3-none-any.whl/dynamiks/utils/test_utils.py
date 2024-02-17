import os
import numpy
import dynamiks
from py_wake.deficit_models.gaussian import NiayifarGaussianDeficit
from py_wake.examples.data.hornsrev1 import V80
from dynamiks.dwm.flow_simulation import DWMFlowSimulation
from dynamiks.dwm.particle_deficit_profiles.pywake_deficit_wrapper import PyWakeDeficitGenerator
from dynamiks.sites._site import TurbulenceFieldSite
from dynamiks.sites.turbulence_fields import RandomTurbulence, MannTurbulenceField
from dynamiks.wind_turbines.pywake_windturbines import PyWakeWindTurbines
from dynamiks.dwm.particle_motion_models import ParticleMotionModel
from dynamiks.dwm.particles_model import WindTurbinesParticles


tfp = os.path.abspath(os.path.dirname(dynamiks.__file__).replace("\\", "/") + '/../tests/test_files') + "/"
npt = numpy.testing


class DefaultDWMFlowSimulation(DWMFlowSimulation):
    def __init__(self, x=[0], y=[0], z=0, ws=10, ti=.1, wd=270, site='mann', windTurbines=None,
                 wakeDeficitModel=None, addedTurbulenceModel=None, dt=1, fc=.1, d_particle=2, n_particles=10, step_handlers=[],
                 particleMotionModel=None, windTurbineParticles_cls=WindTurbinesParticles):

        if site == 'random':
            site = TurbulenceFieldSite(ws=10, ti=ti, turbulenceField=RandomTurbulence(ti=ti, ws=ws))
        elif site == 'mann':
            turbfield = MannTurbulenceField.from_netcdf(
                tfp + "mann_turb/hipersim_mann_l29.4_ae1.0000_g3.9_h0_1024x128x32_3.200x3.20x3.20_s0001.nc",
                offset=(-2500, -100, 20))
            turbfield.scale_TI(ti=ti, U=ws)
            site = TurbulenceFieldSite(ws=ws, ti=ti, turbulenceField=turbfield)
        elif site == 'uniform':
            site = TurbulenceFieldSite(ws=10, ti=ti, turbulenceField=RandomTurbulence(ti=0, ws=ws))

        windTurbines = windTurbines or PyWakeWindTurbines(x=x, y=y, z=z, windTurbine=V80())
        wakeDeficitModel = wakeDeficitModel or PyWakeDeficitGenerator(
            deficitModel=NiayifarGaussianDeficit(use_effective_ws=True), scale_with_freestream=False)
        particleMotionModel = particleMotionModel or ParticleMotionModel(cut_off_frequency=fc)

        DWMFlowSimulation.__init__(self, site=site, windTurbines=windTurbines, dt=dt, wind_direction=wd,
                                   step_handlers=step_handlers,
                                   n_particles=n_particles, d_particle=d_particle,
                                   wakeDeficitModel=wakeDeficitModel,
                                   particleMotionModel=particleMotionModel,
                                   addedTurbulenceModel=addedTurbulenceModel,
                                   windTurbinesParticles_cls=windTurbineParticles_cls,
                                   )
