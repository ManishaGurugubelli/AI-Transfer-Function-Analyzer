import streamlit as st

def show_confidence_meter(prediction):

    st.divider()

    st.subheader("🎯 AI Confidence Analysis")

    probability = prediction["probability"]

    st.progress(probability/100)

    if probability >= 95:

        st.success(
            f"""
### Very High Confidence

Confidence Score : {probability:.2f} %

The AI model is extremely confident in this prediction.

The feature pattern strongly matches the learned dataset.
"""
        )

    elif probability >= 85:

        st.info(
            f"""
### High Confidence

Confidence Score : {probability:.2f} %
"""
        )

    elif probability >= 70:

        st.warning(
            f"""
### Medium Confidence

Confidence Score : {probability:.2f} %
"""
        )

    else:

        st.error(
            f"""
### Low Confidence

Confidence Score : {probability:.2f} %
"""
        )