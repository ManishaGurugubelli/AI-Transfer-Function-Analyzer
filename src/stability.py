import numpy as np


def calculate_poles(denominator):
    """
    Calculate poles of transfer function.
    """

    return np.roots(denominator)


def is_stable(poles):
    """
    Stable if every pole has negative real part.
    """

    return int(np.all(np.real(poles) < 0))