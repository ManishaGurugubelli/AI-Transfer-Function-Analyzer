import numpy as np

from config import *


def generate_order():
    """Randomly choose transfer function order."""
    return np.random.randint(MIN_ORDER, MAX_ORDER + 1)


def generate_numerator(order):
    """
    Generate numerator coefficients.
    Degree is always less than denominator degree.
    """

    degree = np.random.randint(0, order)

    coeffs = np.random.randint(
        NUMERATOR_MIN,
        NUMERATOR_MAX + 1,
        degree + 1
    )

    return coeffs.tolist()


def generate_denominator(order):
    """
    Generate wider denominator coefficients.
    """

    coeffs = [1]

    for _ in range(order):

        value = np.random.randint(
            DENOMINATOR_MIN,
            DENOMINATOR_MAX + 1
        )

        while value == 0:
            value = np.random.randint(
                DENOMINATOR_MIN,
                DENOMINATOR_MAX + 1
            )

        coeffs.append(value)

    return coeffs


def pad_polynomial(coeffs):
    """
    Pad coefficients to fixed length.

    Num5 Num4 Num3 Num2 Num1 Num0
    """

    padded = [0] * (MAX_ORDER + 1)

    start = len(padded) - len(coeffs)

    padded[start:] = coeffs

    return padded


def polynomial_to_string(coeffs, variable="s"):
    """
    Convert coefficient list into readable polynomial.
    """

    degree = len(coeffs) - 1

    terms = []

    for i, c in enumerate(coeffs):

        if c == 0:
            continue

        power = degree - i

        if power > 1:
            terms.append(f"{c}{variable}^{power}")

        elif power == 1:
            terms.append(f"{c}{variable}")

        else:
            terms.append(f"{c}")

    if not terms:
        return "0"

    return " + ".join(terms)