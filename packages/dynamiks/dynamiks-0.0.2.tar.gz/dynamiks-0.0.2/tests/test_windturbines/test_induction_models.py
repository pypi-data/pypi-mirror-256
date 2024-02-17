from dynamiks.wind_turbines.axisymetric_induction import InductionMatch
import matplotlib.pyplot as plt
import numpy as np
from dynamiks.utils.test_utils import npt


def test_InductionMatch():
    r, a = InductionMatch()(1 / 3, 8)
    if 0:
        plt.plot(r, a)
        plt.show()

    print(np.round(a[::50], 2).tolist())
    npt.assert_array_almost_equal(a[::50], [0.0, 0.38, 0.37, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 2)

    r = np.linspace(0, 1, 10)
    r, a = InductionMatch()(1 / 3, 8, r=r)
    print(np.round(a, 2).tolist())
    npt.assert_array_almost_equal(a, [0.0, 0.3, 0.38, 0.38, 0.38, 0.37, 0.37, 0.36, 0.31, 0.0], 2)

    if 0:
        plt.plot(r, a)
        plt.show()
