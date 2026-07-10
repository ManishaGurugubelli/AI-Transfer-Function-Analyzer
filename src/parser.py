import re

MAX_ORDER = 5


def parse_polynomial(poly):
    """
    Convert polynomial string into coefficient list.

    Example:
        s^3+10s^2+120s+500

    Returns:
        [1,10,120,500]
    """

    poly = poly.replace(" ", "")
    poly = poly.replace("-", "+-")

    terms = poly.split("+")

    coeff_dict = {}

    for term in terms:

        if term == "":
            continue

        # Constant term
        if "s" not in term:
            coeff = float(term)
            power = 0

        else:

            # Power
            if "^" in term:
                power = int(term.split("^")[1])
            else:
                power = 1

            coeff_part = term.split("s")[0]

            if coeff_part == "":
                coeff = 1

            elif coeff_part == "-":
                coeff = -1

            else:
                coeff = float(coeff_part)

        coeff_dict[power] = coeff

    highest = max(coeff_dict.keys())

    coeffs = []

    for p in range(highest, -1, -1):

        coeffs.append(coeff_dict.get(p, 0))

    return coeffs


def pad(coeffs):
    """
    Pad coefficient list to MAX_ORDER+1 length.
    """

    padded = [0] * (MAX_ORDER + 1)

    padded[-len(coeffs):] = coeffs

    return padded


def parse_transfer_function(tf):
    """
    Parse transfer function.

    Input:
        (2s+5)/(s^4+6s^3+40s^2+150s+300)

    Returns dictionary.
    """

    tf = tf.replace(" ", "")

    pattern = r"\((.*?)\)/\((.*?)\)"

    match = re.match(pattern, tf)

    if not match:
        raise ValueError("Invalid Transfer Function Format")

    numerator = match.group(1)

    denominator = match.group(2)

    num_coeff = parse_polynomial(numerator)

    den_coeff = parse_polynomial(denominator)

    return {

        "order": len(den_coeff) - 1,

        "numerator": pad(num_coeff),

        "denominator": pad(den_coeff)

    }


if __name__ == "__main__":

    tf = input("Enter Transfer Function : ")

    result = parse_transfer_function(tf)

    print("\nParsed Successfully\n")

    print("Order")

    print(result["order"])

    print("\nNumerator")

    print(result["numerator"])

    print("\nDenominator")

    print(result["denominator"])