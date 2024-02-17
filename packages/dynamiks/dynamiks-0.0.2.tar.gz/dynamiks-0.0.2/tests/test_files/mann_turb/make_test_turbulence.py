from dynamiks.sites.turbulence_fields import MannTurbulenceField
from dynamiks.utils.test_utils import tfp
import hipersim

if __name__ == '__main__':
    default_kwargs = dict(alphaepsilon=1, L=29.4, Gamma=3.9,
                          Nxyz=(1024, 128, 32), dxyz=(1, 1, 1), seed=1, HighFreqComp=0, double_xyz=(0, 0, 0))

    for kwargs in [dict(Nxyz=(256, 8, 8)),
                   dict(Nxyz=(1024, 128, 32), dxyz=(3.2, 3.2, 3.2)),
                   dict(Nxyz=(1024, 128, 32), dxyz=(9.6, 9.6, 9.6))]:

        mtf = hipersim.MannTurbulenceField.generate(**{**default_kwargs, **kwargs})
        mtf.to_netcdf(tfp + 'mann_turb')
