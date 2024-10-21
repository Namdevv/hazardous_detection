import tensorflow as tf
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from icrawler.builtin import BingImageCrawler
from icrawler.builtin import GoogleImageCrawler
import numpy as np
import time

def crawl_images(keyword, num_images, output_dir):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tính số lượng ảnh cần tải từ mỗi nguồn
    bing_images = num_images // 2
    google_images = num_images - bing_images

    # Cấu hình và chạy Bing Image Crawler
    bing_crawler = BingImageCrawler(
        downloader_threads=4,
        storage={'root_dir': os.path.join(output_dir, 'bing')}
    )
    bing_crawler.crawl(keyword=keyword, max_num=bing_images)

    # Cấu hình và chạy Google Image Crawler
    google_crawler = GoogleImageCrawler(
        downloader_threads=4,
        storage={'root_dir': os.path.join(output_dir, 'google')}
    )
    google_crawler.crawl(keyword=keyword, max_num=google_images)

    # Kiểm tra tổng số ảnh đã tải
    total_images = len(os.listdir(os.path.join(output_dir, 'bing'))) + \
                   len(os.listdir(os.path.join(output_dir, 'google')))
    print(f"Tổng số ảnh đã tải: {total_images}")

# Sử dụng hàm
keywords = [
    "dg sticker on container",
    "dangerous goods label on container",
    "hazardous material sticker shipping",
    "container hazard warning label",
    "IMDG code sticker on container"
]

# Sửa đổi phần gọi hàm crawl_images
for keyword in keywords:
    print(f"Đang tìm kiếm ảnh cho từ khóa: {keyword}")
    crawl_images(keyword, 200, f"output_images/{keyword.replace(' ', '_')}")
    time.sleep(5) # Thay đổi từ khóa tìm kiếm tùy ý

model = tf.keras.models.load_model('model/pretrained_image_classification_model.h5')

def classify_image(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  

    predictions = model.predict(img_array)
    predicted_label = np.argmax(predictions, axis=1)[0]
    
    return predicted_label

# Thêm đoạn mã sau vào cuối file
for keyword in keywords:
    output_dir = f"output_images/{keyword.replace(' ', '_')}"
    for source in ['bing', 'google']:
        source_dir = os.path.join(output_dir, source)
        if os.path.exists(source_dir):
            for image_file in os.listdir(source_dir):
                image_path = os.path.join(source_dir, image_file)
                predicted_label = classify_image(image_path, model)
                
                print(f"Ảnh {image_file} từ {source} cho từ khóa '{keyword}' được phân loại vào nhãn: {predicted_label}")
                
                label_folder = os.path.join(output_dir, str(predicted_label))
                os.makedirs(label_folder, exist_ok=True)
                os.rename(image_path, os.path.join(label_folder, image_file))

    print(f"Đã hoàn thành phân loại ảnh cho từ khóa: {keyword}")

print("Đã hoàn thành phân loại tất cả ảnh.")