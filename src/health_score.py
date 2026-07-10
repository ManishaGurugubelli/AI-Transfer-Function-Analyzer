def generate_health_report(prediction, metrics, recommendations):

    score = 100

    problems = []

    suggestions = []

    # -----------------------------
    # Stability
    # -----------------------------

    if prediction["prediction"] == "Unstable":

        score -= 40

        problems.append("Right Half Plane Pole Found")

    # -----------------------------
    # Confidence
    # -----------------------------

    if prediction["probability"] < 90:

        score -= 10

        problems.append("Prediction confidence below 90%")

    # -----------------------------
    # Settling Time
    # -----------------------------

    settling = metrics["Settling Time"]

    if isinstance(settling, (int, float)):

        if settling > 10:

            score -= 10

            problems.append(
                f"Large Settling Time ({settling}s)"
            )

    # -----------------------------
    # Parameter Ranges
    # -----------------------------

    for item in recommendations:

        # No stable interval exists
        if len(item["Intervals"]) == 0:

            score -= 5

            problems.append(
                f"{item['Parameter']} has no stable operating interval."
            )

            continue

        inside = False

        # Check whether current value is inside any interval
        for left, right in item["Intervals"]:

            if left <= item["Current"] <= right:

                inside = True
                break

        # Penalize only if current value is outside
        if not inside:

            score -= 10

            problems.append(
                f"{item['Parameter']} is outside the stable operating interval."
            )

            # Suggest only if value actually changes
            if (
                item["Suggested"] is not None
                and item["Suggested"] != item["Current"]
            ):

                suggestions.append(
                    f"{item['Parameter']} → {item['Suggested']}"
                )

    # Prevent negative score
    score = max(score, 0)

    return {

        "score": score,

        "problems": problems,

        "suggestions": suggestions

    }