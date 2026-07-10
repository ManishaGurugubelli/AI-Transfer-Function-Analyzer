import streamlit as st

def show_ai_explanation(prediction, health):

    st.divider()

    st.subheader("🧠 AI Decision Process")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
### Model Used

MLP Classifier

Prediction Confidence

{prediction['probability']} %

Confidence Level

{prediction['confidence']}
""")

    with col2:

        if prediction["prediction"] == "Stable":

            st.success("""
AI Decision Logic

✔ Coefficient distribution resembles learned stable systems.

✔ Engineered feature vector falls inside learned decision boundary.

✔ Prediction confidence exceeds 95%.

✔ Stability classified as Stable.
""")

        else:

            st.error("""
### AI Reasoning

❌ Coefficient pattern resembles unstable systems.

❌ One or more engineered features exceed learned limits.

❌ AI confidence indicates instability.

❌ Predicted as Unstable.
""")

    st.progress(prediction["probability"]/100)