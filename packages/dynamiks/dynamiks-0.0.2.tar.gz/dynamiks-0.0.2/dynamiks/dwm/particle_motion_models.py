import numpy as np


class CutOffFrq():
    def __init__(self, d):
        self.d = d

    def __call__(self, U, D):
        return U / (self.d * D)


"""Larsen, G. C., Madsen, H. A., Thomsen, K., and Larsen, T. J.
Wake meandering: a pragmatic approach, Wind Energy, 11, 377–395,
https://doi.org/10.1002/we.267, 2008."""
CutOffFrqLarsen2008 = CutOffFrq(2)

"""Lio, W. H., Larsen, G. C., and Thorsen, G. R.:
Dynamic wake tracking using a cost-effective LiDAR and Kalman filtering: Design, simulation and full-scale validation,
Renew Energ., 172, 1073–1086, 2021."""
CutOffFrqLio2021 = CutOffFrq(16)


class ParticleMotionModel():
    def __init__(self, cut_off_frequency, update_initial_speed=True):
        self.update_initial_speed = update_initial_speed
        self._alpha = None
        self.cut_off_frequency = cut_off_frequency

    def initialize(self, flowSimulation):
        if hasattr(self.cut_off_frequency, '__call__'):
            self.cut_off_frequency = self.cut_off_frequency(U=flowSimulation.site.ws,
                                                            D=np.max(flowSimulation.windTurbines.diameter()))
        self.dt = flowSimulation.dt
        self.flowSimulation = flowSimulation

    @property
    def alpha(self):
        if self._alpha is None:

            wc = self.cut_off_frequency * self.dt * 2 * np.pi
            # alpha for low pass filter with <wc> cut-off frequency, see https://dsp.stackexchange.com/a/40465
            self._alpha = np.cos(wc) - 1 + np.sqrt(np.cos(wc) ** 2 - 4 * np.cos(wc) + 3)
        return self._alpha

    def initial_speed(self, windTurbine=None):
        if windTurbine is None:
            return np.array([self.flowSimulation.site.ws, 0, 0], dtype=float)
        return windTurbine.rotor_avg_windspeed(include_wakes=True)[:, 0]

    def __call__(self, position_xip, velocity_uip):
        assert position_xip.shape == velocity_uip.shape
        uvw = self.flowSimulation.get_windspeed(position_xip, include_wakes=False)
        velocity = velocity_uip + self.alpha * (uvw - velocity_uip)  # low pass filter particle velocity
        position = position_xip + velocity * self.flowSimulation.dt
        return position, velocity


class HillVortexParticleMotion(ParticleMotionModel):
    def __call__(self, position_xip, velocity_uip):
        position_xip, velocity_uip = ParticleMotionModel.__call__(self, position_xip, velocity_uip)
        fs = self.flowSimulation
        dt = fs.dt
        for i in range(fs.n_wt):
            m = [p.initial_position is not None for p in fs.windTurbinesParticles[i].particles[0]]
            yaw, tilt = fs.windTurbines[i].yaw_tilt()
            x_p = position_xip[0, i]
            delta_U_w = np.array([p.deficit_norm_magnitude([x - p.initial_position[0]])[0]
                                 for p, x in zip(fs.windTurbinesParticles[i].particles[0][m], x_p[m])])
            y, t = np.deg2rad(yaw), np.deg2rad(tilt)
            # total angle
            total = np.arctan(np.hypot(np.tan(y), np.tan(t)))
            u_def = -0.4 * delta_U_w * np.cos(total)
            v_def = -0.4 * delta_U_w * np.sin(y)
            w_def = 0.4 * delta_U_w * np.sin(t)

            position_xip[:, i, m] += np.array([u_def, v_def, w_def]) * dt
        return position_xip, velocity_uip
