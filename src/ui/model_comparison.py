import streamlit as st
import pandas as pd

def show_model_comparison():

    st.divider()

    st.subheader("📊 Machine Learning Model Performance")

    try:

        df = pd.read_csv("../results/model_results.csv")

        display = df[
    [
        "Rank",
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "ROC_AUC",
        "CV_Accuracy",
        "Overall_Score"
    ]
].copy()
        display["CV_Accuracy"] = (display["CV_Accuracy"] * 100).round(2)
        display["Overall_Score"] = (display["Overall_Score"] * 100).round(2)

        display["Accuracy"] = (display["Accuracy"] * 100).round(2)
        display["Precision"] = (display["Precision"] * 100).round(2)
        display["Recall"] = (display["Recall"] * 100).round(2)
        display["F1"] = (display["F1"] * 100).round(2)
        display["ROC_AUC"] = (display["ROC_AUC"] * 100).round(2)

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.warning("Model comparison file not found.")