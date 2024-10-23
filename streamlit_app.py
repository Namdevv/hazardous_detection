import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import cv2
import numpy as np
from ultralytics import YOLO
import av
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)

class YOLOProcessor(VideoProcessorBase):
    def __init__(self):
        try:
            self.model = YOLO("runs_v2/detect/train/weights/best.pt")
            st.success("Model loaded successfully!")
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            logging.error(f"Model loading error: {str(e)}")

    def recv(self, frame):
        try:
            img = frame.to_ndarray(format="bgr24")
            
            # Thực hiện YOLO detection
            results = self.model(img)
            
            # Vẽ các bounding boxes và labels
            for result in results:
                boxes = result.boxes.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].astype(int)
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = f"{result.names[cls]} {conf:.2f}"
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            return av.VideoFrame.from_ndarray(img, format="bgr24")
        except Exception as e:
            logging.error(f"Error in frame processing: {str(e)}")
            return frame

def main():
    st.set_page_config(
        page_title="YOLO Object Detection",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("YOLO Object Detection - Phone Camera")
    st.write("""
    ### Hướng dẫn sử dụng:
    1. Cho phép trình duyệt truy cập camera
    2. Đợi model YOLO load xong
    3. Di chuyển camera để phát hiện đối tượng
    
    ⚠️ Lưu ý: Ứng dụng yêu cầu kết nối HTTPS để truy cập camera
    """)
    
    # Kiểm tra HTTPS
    if not st.runtime.exists():
        st.warning("⚠️ Vui lòng chạy ứng dụng qua HTTPS hoặc deploy lên Streamlit Cloud")
        
    try:
        webrtc_streamer(
            key="yolo-detection",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=YOLOProcessor,
            rtc_configuration={
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {
                        "urls": ["turn:relay.metered.ca:80"],
                        "username": "your_turn_username",  # Thay thế bằng thông tin TURN server của bạn
                        "credential": "your_turn_password",
                    },
                ]
            },
            media_stream_constraints={
                "video": {"width": {"ideal": 1280}, "height": {"ideal": 720}},
                "audio": False
            },
            async_processing=True,
        )
    except Exception as e:
        st.error(f"Error initializing webcam: {str(e)}")
        logging.error(f"Webcam initialization error: {str(e)}")

if __name__ == "__main__":
    main()