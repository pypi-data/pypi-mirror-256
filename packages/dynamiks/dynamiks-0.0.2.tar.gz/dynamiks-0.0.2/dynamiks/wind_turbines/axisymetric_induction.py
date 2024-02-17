import numpy as np
from scipy import integrate


class InductionMatch():
    """Model the axisymetric induction from rotor average induction including tip and root correction
    This model is extracted from jdwm written by Jaime Liew"""

    def __init__(self, r_max=3, Nr=501, Nb=3, delta=0.1, root_a=1.256):
        self.r_max = r_max
        self.Nr = Nr
        self.Nb = Nb
        self.delta = delta
        self.root_a = root_a

        self._root_b = (np.exp(self.root_a) - 1) / self.root_a

    def _tip_correction(self, x, tsr):
        return (2 / np.pi * np.arccos(np.exp(-self.Nb / 2 * np.sqrt(1 + tsr ** 2) * (1 - x))))

    def _root_correction(self, x):
        return 1 - np.exp(-self.root_a * (x / self.delta) ** self._root_b)

    def __call__(self, a_target, tsr, r=None):
        a_mean = a_target
        # Effect of varying fidelity turbine models on wake loss prediction
        func = (
            lambda x: (self._tip_correction(x, tsr) * self._root_correction(x)) * x
        )
        a_hat = a_mean / (2 * integrate.quad(func, 0, 1)[0])
        if r is None:
            r = np.linspace(0, self.r_max, self.Nr)
        a = np.zeros_like(r)
        a[r <= 1] = (a_hat * self._tip_correction(r[r <= 1], tsr) * self._root_correction(r[r <= 1]))

        return r, a
