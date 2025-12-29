import streamlit as st
import pandas as pd
import numpy as np


if "init" not in st.session_state:
    st.session_state.chart_data = pd.DataFrame(
        np.random.randn(20, 3), columns=["a", "b", "c"]
    )
    st.session_state.map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"],
    )
    st.session_state.init = True



pages = [
    st.Page(
        "home.py",
        title="Home",
        icon=":material/home:"
    ),
    st.Page(
        "data.py",
        title="Data",
        icon=":material/table:"
    ),
    st.Page(
        "charts.py",
        title="Charts",
        icon=":material/insert_chart:"
    ),
    st.Page(
        "information.py",
        title="Information",
        icon=":material/image:"
    ),
    st.Page(
        "chat.py",
        title="Chat",
        icon=":material/chat:"
    ),
    st.Page(
        "status.py",
        title="Status",
        icon=":material/error:"
    ),
]

page = st.navigation(pages)
page.run()

with st.sidebar.container(height=310):
    st.page_link("home.py", label="Home", icon=":material/home:")
    st.write("Welcome to the home page!")
    st.write(
        "Select a page from above. This sidebar thumbnail shows a subset of "
        "elements from each page so you can see the sidebar theme."
    )


#Footnote & EY image
st.sidebar.caption(
    "This application was made at EY, by Shrinivas Deshpande, in 2025"
)
url='https://upload.wikimedia.org/wikipedia/commons/3/34/EY_logo_2019.svg'
st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] + div {{
                position:relative;
                bottom: 0;
                height:55%;
                background-image: url({url});
                background-size: 25% auto;
                background-repeat: no-repeat;
                background-position-x: left;
                background-position-y: bottom;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
