import streamlit as st
import cv2
import numpy as np
import time
import PoseModule as pm

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


def show():
    detector = pm.poseDetector()
    count = 0
    dir = 0
    pTime = 0
    st.header("Leg")
    st.write(
        '<a class="caption blue-button" href="../home" target="_self">← Back</a>',
        unsafe_allow_html=True,
    )
    col1, col2, a, b, c, d, e, f, g = st.columns(9)
    with col1:
        start = st.button(
            "Run",
            key="run_button",
        )

    with col2:
        stop = st.button("Stop")

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while start:
        if stop:
            break
        _, img = camera.read()
        img = cv2.resize(img, (1280, 720))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        # print(lmList)
        if len(lmList) != 0:
            # Right Arm
            angle = detector.findAngle(img, 23, 25, 27)
            # # Left Arm
            angle = detector.findAngle(img, 24, 26, 28)
            per = np.interp(angle, (90, 170), (0, 100))
            bar = np.interp(angle, (100, 170), (650, 100))

            # Check for the dumbbell curls
            color = (255, 0, 255)
            if per == 100:
                color = (0, 255, 0)
                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:
                color = (0, 255, 0)
                if dir == 1:
                    count += 0.5
                    dir = 0
            print(count)

            # Draw Bar
            cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
            cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
            cv2.putText(
                img, f"{int(per)} %", (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4
            )

            # Draw Curl Count
            cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
            cv2.putText(
                img,
                str(int(count)),
                (45, 670),
                cv2.FONT_HERSHEY_PLAIN,
                15,
                (255, 0, 0),
                25,
            )

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(
            img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5
        )

        FRAME_WINDOW.image(img)
    else:
        st.write("Stopped")


show()
