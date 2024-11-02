import streamlit as st
import cv2
import numpy as np
from ultralytics import RTDETR

# Load your model (replace with the path to your model file)
model = RTDETR("path_to_your_model/best.pt")

# Set the title of the app
st.title("Hazardous Object Detection with RTDETR")

# File uploader widget to upload an image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load image file with OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = model(image)

    # Extract boxes and names
    boxes = results[0].boxes
    names = results[0].names

    # Draw boxes on the image
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get box coordinates
        label = names[int(box.cls[0])]         # Get label name
        confidence = box.conf[0]               # Confidence score

        # Draw bounding box and label
        cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image_rgb, f"{label} {confidence:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Display the image in Streamlit
    st.image(image_rgb, caption="Detected Image", use_column_width=True)
