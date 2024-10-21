import tensorflow as tf
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image

model = tf.keras.models.load_model('model/pretrained_image_classification_model.h5')

def classify_image(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)g
    img_array = preprocess_input(img_array)  

    predictions = model.predict(img_array)
    predicted_label = np.argmax(predictions, axis=1)[0]
    
    return predicted_label

input_folder = r"C:\Users\Admin\Downloads\www.bing.com\dangerous label on the container - Search Images - 10_19_2024 2-42-45 PM"  
output_folder = r"C:\Users\Admin\Downloads\www.bing.com\classified_images" 

os.makedirs(output_folder, exist_ok=True)

for image_file in os.listdir(input_folder):
    image_path = os.path.join(input_folder, image_file)
    
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        try:
            with Image.open(image_path) as img:
                img.verify() 
            
            predicted_label = classify_image(image_path, model)
            
            print(f"Ảnh {image_file} được phân loại vào nhãn: {predicted_label}")
            
            label_folder = os.path.join(output_folder, str(predicted_label))
            os.makedirs(label_folder, exist_ok=True)
            
            os.rename(image_path, os.path.join(label_folder, image_file))
        except (IOError, SyntaxError) as e:
            print(f"Bỏ qua file {image_file}: Không phải là file ảnh hợp lệ")
            continue

print("Đã hoàn thành phân loại tất cả ảnh.")