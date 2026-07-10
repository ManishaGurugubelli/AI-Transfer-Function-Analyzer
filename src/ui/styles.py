import streamlit as st


def load_css():

    st.markdown(
        """
        <style>

        .main{
            background-color:#F5F7FA;
        }

        h1{
            color:#003366;
            text-align:center;
            font-weight:bold;
        }

        h2,h3{
            color:#004C99;
        }

        div[data-testid="metric-container"]{

            background:white;

            border-radius:12px;

            padding:15px;

            border:1px solid #E0E0E0;

            box-shadow:0px 2px 8px rgba(0,0,0,0.08);

            text-align:center;
        }

        .stButton>button{

            width:100%;

            border-radius:10px;

            background:#1976D2;

            color:white;

            height:50px;

            font-size:18px;

            font-weight:bold;
        }

        .stButton>button:hover{

            background:#0D47A1;

            color:white;

        }

        </style>
        """,
        unsafe_allow_html=True
    )