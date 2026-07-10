import streamlit as st
import matplotlib.pyplot as plt


def show_plots(analysis):

    st.divider()

    st.subheader("📈 System Response")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Pole Map")

        st.pyplot(
            analysis["pole_plot"],
            clear_figure=True
        )

    with col2:

        st.markdown("### Step Response")

        st.pyplot(
            analysis["step_plot"],
            clear_figure=True
        )

    st.markdown("### Impulse Response")

    st.pyplot(
        analysis["impulse_plot"],
        clear_figure=True
    )

    plt.close("all")