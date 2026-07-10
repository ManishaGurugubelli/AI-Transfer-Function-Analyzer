import copy
import numpy as np

from parser import parse_transfer_function
from stability import calculate_poles, is_stable
from config import OPTIMIZER_MAX_RANGE

# ==========================================================
# PARAMETER NAMES
# ==========================================================

PARAMETERS = {

    0: "s⁵",
    1: "s⁴",
    2: "s³",
    3: "s²",
    4: "s",
    5: "Constant"

}
# ==========================================================
# CHECK STABILITY USING POLES
# ==========================================================

def pole_is_stable(denominator):

    # Remove leading zeros (parser pads coefficients)
    denominator = np.trim_zeros(
        denominator,
        trim="f"
    )

    if len(denominator) <= 1:
        return False

    poles = calculate_poles(denominator)

    return bool(is_stable(poles))
# ==========================================================
# FIND CONTINUOUS STABLE INTERVALS (FAST)
# ==========================================================

def find_stable_intervals(order, numerator, denominator, idx):

    COARSE_STEP = 5

    stable_values = []

    coarse_values = []

    # ------------------------------------------------------
    # COARSE SEARCH
    # ------------------------------------------------------

    for value in range(1, OPTIMIZER_MAX_RANGE + 1, COARSE_STEP):

        temp = copy.deepcopy(denominator)
        temp[idx] = value

        stable = pole_is_stable(temp)

        coarse_values.append((value, stable))

    # ------------------------------------------------------
    # FINE SEARCH ONLY NEAR TRANSITIONS
    # ------------------------------------------------------

    tested = set()

    for i in range(len(coarse_values) - 1):

        left_value, left_state = coarse_values[i]
        right_value, right_state = coarse_values[i + 1]

        # Search around transitions
        if left_state != right_state:

            for value in range(left_value, right_value + 1):

                temp = copy.deepcopy(denominator)
                temp[idx] = value

                if pole_is_stable(temp):

                    stable_values.append(value)

                tested.add(value)

        # Entire coarse block is stable
        elif left_state:

            for value in range(left_value, right_value + 1):

                stable_values.append(value)

                tested.add(value)

    # Check last coarse point
    last_value, last_state = coarse_values[-1]

    if last_state:

        for value in range(last_value, OPTIMIZER_MAX_RANGE + 1):

            stable_values.append(value)

    stable_values = sorted(set(stable_values))

    # ------------------------------------------------------
    # Merge consecutive values
    # ------------------------------------------------------

    if len(stable_values) == 0:
        return []

    intervals = []

    start = stable_values[0]
    end = stable_values[0]

    for value in stable_values[1:]:

        if value == end + 1:

            end = value

        else:

            intervals.append((start, end))

            start = value
            end = value

    intervals.append((start, end))

    return intervals
# ==========================================================
# PARAMETER OPTIMIZER
# ==========================================================

def optimize_transfer_function(tf):

    parsed = parse_transfer_function(tf)

    order = parsed["order"]
    numerator = parsed["numerator"]
    denominator = parsed["denominator"]

    recommendations = []

    # --------------------------------------------
    # Denominator coefficients only
    # --------------------------------------------

    start_index = 6 - (order + 1)

    for idx in range(start_index, 6):

        current = denominator[idx]

        intervals = find_stable_intervals(

            order,
            numerator,
            denominator,
            idx

        )

        interval_strings = [

            f"{left} - {right}"

            for left, right in intervals

        ]

        inside = False

        suggested = None

        # --------------------------------------------
        # Check if current value is inside interval
        # --------------------------------------------

        for left, right in intervals:

            if left <= current <= right:

                inside = True

                suggested = current

                break

        # --------------------------------------------
        # Find nearest boundary
        # --------------------------------------------

        if not inside and intervals:

            best_distance = float("inf")

            for left, right in intervals:

                if abs(current - left) < best_distance:

                    best_distance = abs(current - left)

                    suggested = left

                if abs(current - right) < best_distance:

                    best_distance = abs(current - right)

                    suggested = right

        recommendations.append({

            "Parameter": PARAMETERS[idx],

            "Current": current,

            "Intervals": intervals,

            "Interval_List": interval_strings,

            "Stable_Range":

                ", ".join(interval_strings)

                if interval_strings

                else "No Stable Interval",

            "Suggested": suggested,

            "Status":

                "✅ Inside Stable Interval"

                if inside

                else "⚠ Outside Stable Interval"

                if interval_strings

                else "❌ No Stable Interval",

            "Count": len(intervals)

        })

    return {

        "prediction": None,

        "recommendations": recommendations

    }
if __name__ == "__main__":

    tf = input("Enter Transfer Function : ")

    result = optimize_transfer_function(tf)

    print(result)
