import joblib
import numpy as np

from parser import parse_transfer_function
from features import create_feature_vector

# ==========================================
# LOAD MODEL
# ==========================================

MODEL = joblib.load("../models/best_model.pkl")
FEATURE_NAMES = joblib.load("../models/feature_names.pkl")


# ==========================================
# CONFIDENCE
# ==========================================

def get_confidence(probability):

    if probability >= 0.95:
        return "Very High"

    elif probability >= 0.85:
        return "High"

    elif probability >= 0.70:
        return "Medium"

    return "Low"


# ==========================================
# PREDICT FROM COEFFICIENTS
# ==========================================

def predict_from_coefficients(order, numerator, denominator):

    features = create_feature_vector(
        order,
        numerator,
        denominator
    )

    features = features[FEATURE_NAMES]

    prediction = MODEL.predict(features)[0]

    probability = MODEL.predict_proba(features)[0]

    confidence = max(probability)

    return {

        "prediction": "Stable" if prediction else "Unstable",

        "probability": round(confidence*100,2),

        "confidence": get_confidence(confidence)

    }


# ==========================================
# PREDICT FROM TF STRING
# ==========================================

def predict_transfer_function(tf):

    parsed = parse_transfer_function(tf)

    result = predict_from_coefficients(

        parsed["order"],

        parsed["numerator"],

        parsed["denominator"]

    )

    poles = np.roots(

        [x for x in parsed["denominator"] if x!=0]

    )

    result["order"] = parsed["order"]

    result["poles"] = poles

    return result