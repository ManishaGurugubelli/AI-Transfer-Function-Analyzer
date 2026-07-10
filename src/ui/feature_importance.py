import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

def show_feature_importance():

    st.divider()

    st.subheader("📈 AI Feature Importance")

    try:

        model = joblib.load("../models/best_model.pkl")
        feature_names = joblib.load("../models/feature_names.pkl")

        importances = None

        # Tree-based models
        if hasattr(model, "feature_importances_"):

            importances = model.feature_importances_

        # Pipeline (Random Forest / Gradient Boosting in Pipeline)
        elif hasattr(model, "named_steps"):

            last = list(model.named_steps.values())[-1]

            if hasattr(last, "feature_importances_"):
                importances = last.feature_importances_

        if importances is None:

            st.info(
                "Feature importance is not directly available for this model."
            )
            return

        df = pd.DataFrame({

            "Feature": feature_names,
            "Importance": importances

        })

        df = df.sort_values(
            "Importance",
            ascending=False
        ).head(10)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        fig, ax = plt.subplots(figsize=(8,5))

        ax.barh(
            df["Feature"],
            df["Importance"]
        )

        ax.invert_yaxis()

        ax.set_xlabel("Importance")

        ax.set_title("Top 10 AI Features")

        st.pyplot(fig)

    except Exception as e:

        st.warning(e)