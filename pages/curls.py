import streamlit as st
import cv2
import numpy as np
import PoseModule as pm
import time
from streamlit_webrtc import *
import av


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


detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
st.header("Curls")
st.write(
    '<a class="caption blue-button" href="../home" target="_self">← Back</a>',
    unsafe_allow_html=True,
)


cnt = 0
dir = 0
pTime = 0


def video_frame_callback(frame: av.VideoFrame):
    global cnt, dir, pTime

    frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
    # Draw a rectangle on the frame
    frame = detector.findPose(frame, False)
    lmList = detector.findPosition(frame, False)

    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(frame, 12, 14, 16)
        # # Left Arm
        angle = detector.findAngle(frame, 11, 13, 15)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
        color = (255, 0, 255)

        if per == 100:
            if dir == 0:
                cnt += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                cnt += 0.5
                dir = 0
        print(cnt)
        cv2.rectangle(frame, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(frame, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(
            frame, f"{int(per)} %", (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4
        )
        cv2.rectangle(frame, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(
            frame,
            str(int(cnt)),
            (45, 670),
            cv2.FONT_HERSHEY_PLAIN,
            15,
            (255, 0, 0),
            25,
        )

    return av.VideoFrame.from_ndarray(
        frame, format="rgb24"
    )  # Encode and return BGR frame


detector = pm.poseDetector()
ctx = webrtc_streamer(
    key="Squats-pose-analysis",
    video_frame_callback=video_frame_callback,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },  # Add this config
    media_stream_constraints={
        "video": {
            "width": {"min": 1280, "ideal": 1280},
            "height": {"min": 720, "ideal": 720},
        },
        "audio": False,
    },
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=True, muted=False),
)
