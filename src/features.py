from pyexpat import features

import numpy as np
import pandas as pd
def compute_features(order, numerator, denominator):

    # Ensure fixed length
    # Convert to list
    numerator = list(numerator)
    denominator = list(denominator)

    # Pad numerator to length 6
    numerator = [0] * (6 - len(numerator)) + numerator

    # Pad denominator to length 6
    denominator = [0] * (6 - len(denominator)) + denominator


    coeffs = np.array(numerator + denominator, dtype=float)

    features = {}

    # =====================================================
    # BASIC FEATURES
    # =====================================================

    features["Order"] = order

    for i in range(6):
        features[f"Num{i}"] = numerator[i]

    for i in range(6):
        features[f"Den{i}"] = denominator[i]

    # =====================================================
    # STATISTICAL FEATURES
    # =====================================================

    features["Coeff_Max"] = np.max(coeffs)
    features["Coeff_Min"] = np.min(coeffs)
    features["Coeff_Mean"] = np.mean(coeffs)
    features["Coeff_STD"] = np.std(coeffs)
    features["Coeff_Variance"] = np.var(coeffs)
    features["Coeff_Sum"] = np.sum(coeffs)

    # =====================================================
    # ENGINEERED FEATURES
    # =====================================================

    features["Coeff_Range"] = (
        features["Coeff_Max"] -
        features["Coeff_Min"]
    )

    features["Coeff_L1"] = np.sum(np.abs(coeffs))

    features["Coeff_L2"] = np.sqrt(np.sum(coeffs ** 2))

    features["Coeff_RMS"] = np.sqrt(np.mean(coeffs ** 2))

    features["Coeff_Median"] = np.median(coeffs)

    features["Coeff_NonZero"] = np.count_nonzero(coeffs)

    features["Zero_Coeff_Count"] = np.sum(coeffs == 0)

    features["Positive_Coeff"] = np.sum(coeffs > 0)

    features["Negative_Coeff"] = np.sum(coeffs < 0)

    features["Num_NonZero"] = np.count_nonzero(numerator)

    features["Den_NonZero"] = np.count_nonzero(denominator)

    features["Leading_Num"] = next(
        (x for x in numerator if x != 0),
        0
    )

    features["Constant_Num"] = numerator[-1]

    features["Leading_Den"] = next(
        (x for x in denominator if x != 0),
        0
    )

    features["Constant_Den"] = denominator[-1]

    features["Num_Mean"] = np.mean(numerator)

    features["Den_Mean"] = np.mean(denominator)

    features["Num_STD"] = np.std(numerator)

    features["Den_STD"] = np.std(denominator)

    # =====================================================
    # COEFFICIENT RATIO
    # =====================================================

    denominator_value = features["Coeff_Min"] + 1

    if abs(denominator_value) < 1e-12:

        features["Coeff_Ratio"] = 0

    else:

        features["Coeff_Ratio"] = (
            (features["Coeff_Max"] + 1)
            / denominator_value
        )

    # =====================================================
    # NORMALIZED DENOMINATOR
    # =====================================================

    den = np.array(denominator, dtype=float)

    if np.max(np.abs(den)) > 0:

        den_norm = den / np.max(np.abs(den))

    else:

        den_norm = den

    for i in range(6):

        features[f"NormDen{i}"] = den_norm[i]

    # =====================================================
    # DENOMINATOR RATIOS
    # =====================================================

    for i in range(5):

        if denominator[i + 1] != 0:

            features[f"Ratio_{i}"] = (
                denominator[i] /
                denominator[i + 1]
            )

        else:

            features[f"Ratio_{i}"] = 0

    # =====================================================
    # LOG DENOMINATOR
    # =====================================================

    for i in range(6):

        features[f"LogDen{i}"] = np.log1p(
            abs(denominator[i])
        )

    return features
# =====================================================
# DATASET FEATURE EXTRACTION
# =====================================================

def extract_features(order, numerator, denominator, poles):

    # poles parameter kept only for compatibility

    return compute_features(
        order,
        numerator,
        denominator
    )


# =====================================================
# PREDICTION FEATURE EXTRACTION
# =====================================================

def create_feature_vector(order, numerator, denominator):

    features = compute_features(
        order,
        numerator,
        denominator
    )

    return pd.DataFrame([features])