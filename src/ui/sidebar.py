import streamlit as st

def show_sidebar():

    # ==========================================================
    # TITLE
    # ==========================================================

    st.sidebar.title("🤖 AI Dashboard")

    st.sidebar.caption(
        "AI-Assisted Transfer Function Stability and Relative Stability Analyzer"
    )

    st.sidebar.markdown("---")

    # ==========================================================
    # MODEL INFORMATION
    # ==========================================================

    st.sidebar.subheader("🏆 Best AI Model")

    st.sidebar.success("MLP Classifier")

    st.sidebar.metric(
        "🎯 Training Accuracy",
        "99.53%"
    )

    st.sidebar.metric(
        "📈 Cross Validation",
        "99.39%"
    )

    st.sidebar.metric(
        "📊 Dataset",
        "30,000 Samples"
    )

    st.sidebar.metric(
        "⚙️ Features",
        "56 Engineered"
    )

    st.sidebar.markdown("---")

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    st.sidebar.subheader("🎯 Confidence Scale")

    st.sidebar.info("""
🟢 **Very High** : ≥95%

🟡 **High** : 85–95%

🟠 **Medium** : 70–85%

🔴 **Low** : <70%
""")

    st.sidebar.markdown("---")

    # ==========================================================
    # AI MODULES
    # ==========================================================

    st.sidebar.subheader("🧠 AI Modules")

    st.sidebar.markdown("""
✅ Stability Prediction

✅ Relative Stability Comparator

✅ Multi-Model Learning

✅ Confidence Estimation

✅ Engineering Recommendation
""")

    st.sidebar.markdown("---")

    # ==========================================================
    # CONTROL SYSTEM MODULES
    # ==========================================================

    st.sidebar.subheader("⚙️ Control System Modules")

    st.sidebar.markdown("""
✔ Pole Analysis

✔ Step Response

✔ Impulse Response

✔ Pole-Zero Plot

✔ Stable Interval Detection

✔ Health Assessment
""")

    st.sidebar.markdown("---")

    # ==========================================================
    # TECH STACK
    # ==========================================================

    st.sidebar.subheader("🛠 Tech Stack")

    st.sidebar.markdown("""
- Python

- Streamlit

- Scikit-Learn

- NumPy

- Pandas

- Matplotlib

- Control Systems
""")

    st.sidebar.markdown("---")

    # ==========================================================
    # PROJECT INFO
    # ==========================================================

    st.sidebar.subheader("📌 Developed by")

    st.sidebar.success("""
Manisha Gurugubelli
""")
