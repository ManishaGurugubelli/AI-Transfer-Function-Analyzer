import streamlit as st
import pandas as pd
import joblib

def show_training_dashboard():

    st.divider()

    st.subheader("📊 AI Training Dashboard")

    try:

        df = pd.read_csv("../results/model_results.csv")

        best = df.iloc[0]

        feature_names = joblib.load("models/feature_names.pkl")

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1:
            st.metric("Best Model", best["Model"])

        with c2:
            st.metric(
                "Training Accuracy",
                f"{best['Accuracy']*100:.2f}%"
            )

        with c3:
            st.metric(
                "Cross Validation",
                f"{best['CV_Accuracy']*100:.2f}%"
            )

        with c4:
            st.metric(
                "AI vs Pole",
                "95.30%"
            )

        with c5:
            st.metric(
                "Dataset",
                "30,000"
            )

        with c6:
            st.metric(
                "Features",
                len(feature_names)
            )

        st.bar_chart(
            df.set_index("Model")["Accuracy"]
        )

        st.caption(
            "AI vs Pole Analysis: 95.30% agreement on 1000 unseen transfer functions."
        )

    except Exception as e:

        st.warning(e)