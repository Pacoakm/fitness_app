import streamlit as st
import squat


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
        display: inline-block;
        padding: 10px 20px;
        background-color: transparent;
        color: rgb(0, 104, 201);
        border: 2.5px solid rgb(0, 104, 201);
        border-radius: 10px;
        text-align: center;
        text-decoration: none;
        cursor: pointer;
        font-weight: bold;
    }
    </style>
"""

st.markdown(caption_style, unsafe_allow_html=True)
st.markdown(button_style, unsafe_allow_html=True)
st.title("Fitness trainer")
# option = st.sidebar.selectbox("Choose page", ["Home", "squat", "curls"])
st.write(
    '<a class="caption blue-button" href=".." target="_self">← Back to home</a>',
    unsafe_allow_html=True,
)
option = 0
if option == "squat":
    squat.show()
elif option == "curls":
    curls.show()
else:
    squat_image_path = "/Users/pacoakm/Documents/AI/squat.png"
    curls_image_path = "/Users/pacoakm/Documents/AI/Seniors_Exercise.jpg"
    leg_image_path = "/Users/pacoakm/Documents/AI/leg.jpeg"

    col1, col2 = st.columns(2)

    with col1:
        st.image(squat_image_path, use_column_width=True)

        st.write(
            '<a class="blue-button caption" href="./squat" target="_self">Squatting →</a>',
            unsafe_allow_html=True,
        )
    with col2:
        st.image(
            "/Users/pacoakm/Documents/AI/Seniors_Exercise.jpg", use_column_width=True
        )
        st.write(
            '<a class="blue-button caption" href="./curls" target="_self">Curls →</a>',
            unsafe_allow_html=True,
        )
    with col1:
        st.image(leg_image_path, use_column_width=True)

        st.write(
            '<a class="blue-button caption" href="./leg" target="_self">Leg →</a>',
            unsafe_allow_html=True,
        )
    with col2:
        pass
