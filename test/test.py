import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, RTCConfiguration
import streamlit as st
import cv2
import numpy as np
import time
import PoseModule as pm


# Define a class to process video frames
class PoseEstimationTransformer(VideoTransformerBase):
    def __init__(self):
        self.detector = pm.poseDetector()  # Replace with your pose detection code

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.resize(img, (1280, 720))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.detector.findPose(img, False)
        lmList = self.detector.findPosition(img, False)
        if len(lmList) != 0:
            # Right Arm
            angle = self.detector.findAngle(img, 12, 14, 16)
            # # Left Arm
            angle = self.detector.findAngle(img, 11, 13, 15)
            per = np.interp(angle, (210, 310), (0, 100))
            bar = np.interp(angle, (220, 310), (650, 100))

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

        return img


# Configure WebRTC
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


# Run the Streamlit app
def main():
    st.title("Pose Detection with Streamlit and WebRTC")

    webrtc_ctx = webrtc_streamer(
        key="pose-detection",
        video_transformer_factory=PoseEstimationTransformer,
        rtc_configuration=rtc_configuration,
        async_transform=True,
    )

    if not webrtc_ctx.state.playing:
        st.write("Waiting for webcam feed...")


if __name__ == "__main__":
    main()
