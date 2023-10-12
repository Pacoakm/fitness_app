import streamlit as st


st.set_page_config(
    initial_sidebar_state="collapsed",
)
caption_style = """
    <style>
    .caption {
        font-size: 24px;
        color: black;
    }
    </style>
"""
button_style = """
    <style>
    .blue-button {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        padding: 10px 20px;
        background-color: transparent;
        color: rgb(0, 104, 201);
        border: 2.5px solid rgb(0, 104, 201);
        border-radius: 10px;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        font-weight: bold;
        width: 300px;
        height: 400px;
    }
    </style>
"""

st.markdown(caption_style, unsafe_allow_html=True)
st.markdown(button_style, unsafe_allow_html=True)
st.title("Fitness trainer")
# option = st.sidebar.selectbox("Choose page", ["Home", "squat", "curls"])

squat_image_path = "/Users/pacoakm/Documents/AI/squat.png"
curls_image_path = "/Users/pacoakm/Documents/AI/Seniors_Exercise.jpg"
leg_image_path = "/Users/pacoakm/Documents/AI/leg.jpeg"

col1, col2 = st.columns(2)

with col1:
    st.write(
        '<a class="blue-button caption" href="./home" target="_self">Start →</a>',
        unsafe_allow_html=True,
    )
with col2:
    st.write(
        '<a class="blue-button caption" href="./ocr" target="_self">Nutrition info →</a>',
        unsafe_allow_html=True,
    )
