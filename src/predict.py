import numpy as np

from parser import parse_transfer_function
from predict_core import predict_transfer_function
from visualization import analyze_and_visualize
from parameter_optimizer import optimize_transfer_function
from health_score import generate_health_report


# ==========================================================
# MAIN
# ==========================================================

def main():

    tf = input("\nEnter Transfer Function : ")

    # -------------------------------------------------
    # AI Prediction
    # -------------------------------------------------

    result = predict_transfer_function(tf)

    print("\n" + "=" * 60)
    print("AI TRANSFER FUNCTION ANALYZER")
    print("=" * 60)

    print(f"Prediction   : {result['prediction']}")
    print(f"Probability  : {result['probability']} %")
    print(f"Confidence   : {result['confidence']}")
    print(f"Order        : {result['order']}")

    print("\nPole Locations")
    print("-" * 60)

    for pole in result["poles"]:
        print(pole)

    # -------------------------------------------------
    # Visualization
    # -------------------------------------------------

    parsed = parse_transfer_function(tf)

    print("\nGenerating System Analysis...")

    analysis = analyze_and_visualize(
        parsed["numerator"],
        parsed["denominator"],
        result["poles"]
    )

    # -------------------------------------------------
    # Parameter Optimization
    # -------------------------------------------------

    recommendation = optimize_transfer_function(tf)

    # -------------------------------------------------
    # Health Score
    # -------------------------------------------------

    health = generate_health_report(
        result,
        analysis["metrics"],
        recommendation["recommendations"]
    )

    print("\n" + "=" * 60)
    print("AI SYSTEM HEALTH SCORE")
    print("=" * 60)

    print(f"\nOverall Health Score : {health['score']} / 100")

    if health["score"] >= 90:
        print("Status : Excellent")
    elif health["score"] >= 75:
        print("Status : Good")
    elif health["score"] >= 50:
        print("Status : Fair")
    else:
        print("Status : Critical")

    print("\nDetected Problems")
    print("-" * 60)

    if len(health["problems"]) == 0:

        print("✔ No major issues detected.")

    else:

        for problem in health["problems"]:
            print(f"❌ {problem}")

    print("\nAI Suggestions")
    print("-" * 60)

    if len(health["suggestions"]) == 0:

        print("✔ No tuning required.")

    else:

        for suggestion in health["suggestions"]:
            print(f"➡ {suggestion}")

    # -------------------------------------------------
    # Parameter Stability Table
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("PARAMETER STABILITY RANGES")
    print("=" * 60)

    print(f"{'Parameter':<15}{'Current':<12}{'Stable Range':<22}{'Suggested':<12}{'Status'}")
    print("-" * 85)

    if len(recommendation["recommendations"]) == 0:

        print("No recommendations available.")

    else:

        for item in recommendation["recommendations"]:

            if item["Stable_Min"] is None:

                stable_range = "None"
                suggested = "-"
                status = "❌ No Stable Range"

            else:

                stable_range = f"{item['Stable_Min']} - {item['Stable_Max']}"
                suggested = item["Suggested"]

                inside = (
                    item["Stable_Min"] <= item["Current"] <= item["Stable_Max"]
                )

                status = "✅ Inside" if inside else "❌ Outside"

            print(
                f"{item['Parameter']:<15}"
                f"{str(item['Current']):<12}"
                f"{stable_range:<22}"
                f"{str(suggested):<12}"
                f"{status}"
            )

    print("\n" + "=" * 60)
    print("Analysis Completed Successfully!")
    print("=" * 60)


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    main()