import joblib
import numpy as np
import pandas as pd

from generator import pad_polynomial
from stability import calculate_poles
from features import extract_features

# ==========================================================
# LOAD MODEL
# ==========================================================

print("=" * 60)
print("LOADING RELATIVE STABILITY MODEL")
print("=" * 60)

model = joblib.load("../models/relative_model.pkl")
scaler = joblib.load("../models/relative_scaler.pkl")

print("Relative Stability Model Loaded Successfully!")

# ==========================================================
# PREDICT DOMINANT POLE
# ==========================================================

def predict_relative_stability(numerator, denominator):
    """
    Predict the dominant pole using the trained MLP regressor.

    Parameters
    ----------
    numerator : list
        Numerator coefficients.

    denominator : list
        Denominator coefficients.

    Returns
    -------
    float
        Predicted dominant pole.
    """

    # ---------------------------------------------
    # Order
    # ---------------------------------------------

    order = len(denominator) - 1

    # ---------------------------------------------
    # Calculate poles
    # ---------------------------------------------

    poles = calculate_poles(denominator)

    # ---------------------------------------------
    # Pad coefficients
    # ---------------------------------------------

    numerator_pad = pad_polynomial(numerator)
    denominator_pad = pad_polynomial(denominator)

    # ---------------------------------------------
    # Feature Extraction
    # ---------------------------------------------

    features = extract_features(
        order,
        numerator_pad,
        denominator_pad,
        poles,
    )

    # ---------------------------------------------
    # DataFrame
    # ---------------------------------------------

    X = pd.DataFrame([features])
    print("\nFEATURE VECTOR")
    print(X.T)

    # ---------------------------------------------
    # Handle Inf / NaN
    # ---------------------------------------------

    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)

    # ---------------------------------------------
    # Scale
    # ---------------------------------------------
    print(X.columns.tolist())

    X = scaler.transform(X)
    

    # ---------------------------------------------
    # Prediction
    # ---------------------------------------------

    dominant_pole = model.predict(X)[0]

    return float(dominant_pole)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    numerator = [1]

    denominator = [1, 10, 35, 50]

    prediction = predict_relative_stability(
        numerator,
        denominator
    )

    print("\n" + "=" * 60)
    print("AI DOMINANT POLE PREDICTION")
    print("=" * 60)

    print(f"\nPredicted Dominant Pole : {prediction:.6f}")