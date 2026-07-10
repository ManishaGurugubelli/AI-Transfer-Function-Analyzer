import joblib
import numpy as np
import pandas as pd

from features import create_feature_vector
def build_pairwise_features(order_a, num_a, den_a,
                            order_b, num_b, den_b):

    # Create feature vectors
    A = create_feature_vector(order_a, num_a, den_a)
    B = create_feature_vector(order_b, num_b, den_b)

    row = {}

    for col in A.columns:
        row[f"A_{col}"] = A.iloc[0][col]

    for col in B.columns:
        row[f"B_{col}"] = B.iloc[0][col]

    X = pd.DataFrame([row])

    # Keep training feature order
    X = X[feature_names]

    X = scaler.transform(X)

    return X
    

# ==========================================================
# LOAD MODEL
# ==========================================================

print("=" * 60)
print("LOADING PAIRWISE MODEL")
print("=" * 60)

model = joblib.load("models/pairwise_model.pkl")

scaler = joblib.load("models/pairwise_scaler.pkl")

feature_names = joblib.load("models/pairwise_feature_names.pkl")

print("Pairwise Model Loaded Successfully!")
# ==========================================================
# AI PREDICTION
# ==========================================================

def predict_pairwise(order_a, num_a, den_a,
                     order_b, num_b, den_b):

    # ==========================================================
    # IDENTICAL SYSTEM CHECK
    # ==========================================================

    if (
        order_a == order_b
        and np.allclose(num_a, num_b)
        and np.allclose(den_a, den_b)
    ):
        return "Equivalent Systems", 100.0

    X = build_pairwise_features(
        order_a,
        num_a,
        den_a,
        order_b,
        num_b,
        den_b
    )

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0]

    confidence = np.max(probability) * 100

    if prediction == 0:
        winner = "System A"
    else:
        winner = "System B"

    return winner, confidence
# ==========================================================
# SELF TEST
# ==========================================================

if __name__ == "__main__":

    winner, confidence = predict_pairwise(

        3,
        [0,0,0,0,0,5],
        [0,0,1,10,120,500],

        3,
        [0,0,0,0,0,5],
        [0,0,1,20,250,1000]

    )

    print("\n" + "="*60)
    print("AI RELATIVE STABILITY")
    print("="*60)

    print("Winner     :", winner)
    print(f"Confidence : {confidence:.2f}%")
