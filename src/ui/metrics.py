import streamlit as st


def show_metrics(prediction, health):

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if prediction["prediction"] == "Stable":

            st.success("✅ STABLE")

        else:

            st.error("❌ UNSTABLE")

    with c2:

        st.metric(

            "Probability",

            f"{prediction['probability']} %"

        )

    with c3:

        st.metric(

            "Confidence",

            prediction["confidence"]

        )

    with c4:

        score = health["score"]

        st.metric(

            "Health Score",

            f"{score}/100"

        )

        st.progress(score / 100)