import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import cv2
import av
import numpy as np
from ultralytics import YOLO
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the YOLO model
@st.cache_resource
def load_model():
    return YOLO("runs_v2/detect/train/weights/best.pt")

model = load_model()

# Streamlit App Title
st.title("YOLO Detection via Webcam")

# Video transformer class for real-time detection
class YOLOVideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Perform YOLO detection
        results = model(img)
        
        # Draw bounding boxes and labels on the image
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].astype(int)
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = f"{model.names[cls]} {conf:.2f}"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Webrtc streamer
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

try:
    webrtc_ctx = webrtc_streamer(
        key="YOLO",
        video_transformer_factory=YOLOVideoTransformer,
        async_transform=True,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"video": True, "audio": False},
    )
    
    if webrtc_ctx.video_transformer:
        st.write("WebRTC connection established successfully.")
    else:
        st.warning("WebRTC video transformer is not initialized. Please check your camera and browser settings.")
        
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    logging.exception("Exception in webrtc_streamer")
    st.info("If you're running locally, make sure to use HTTPS. Run with: streamlit run streamlit_app.py --server.sslCert=cert.pem --server.sslKey=key.pem")

# Additional description
st.write("Using YOLO to detect objects from your webcam feed.")

# Add a note about HTTPS requirement
st.info("Note: This app requires a secure connection (HTTPS) to access the webcam. If you're running locally, use the command mentioned above to run with HTTPS.")

# Display WebRTC state
if webrtc_ctx is not None:
    if webrtc_ctx.state.playing:
        st.write("WebRTC is currently playing.")
    else:
        st.write("WebRTC is not playing. Please start the stream.")

    # Display any WebRTC errors
    if hasattr(webrtc_ctx.state, 'error'):
        if webrtc_ctx.state.error:
            st.error(f"WebRTC error: {webrtc_ctx.state.error}")
else:
    st.warning("WebRTC context is not available. There might be an issue with the WebRTC setup.")