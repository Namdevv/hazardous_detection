import os
import cv2
import matplotlib.pyplot as plt
import random
from classname import class_names
import torch
device = "cuda" if torch.cuda.is_available() else "cpu" 

def visualize_image_and_label(image_folder, label_folder, class_names):
    for image_filename in os.listdir(image_folder):
        if image_filename.endswith('.jpg') or image_filename.endswith('.png'):
            image_path = os.path.join(image_folder, image_filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Warning: Unable to read image {image_filename}. Skipping.")
                continue 

            label_filename = image_filename.replace('.jpg', '.txt').replace('.png', '.txt')
            label_path = os.path.join(label_folder, label_filename)

            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    lines = f.readlines()

                for line in lines: 
                    values = line.strip().split()
                    print(values)
                    try:
                        class_id = int(values[0])  
                        x_center, y_center, bbox_width, bbox_height = map(float, values[1:5])  
                        
                        if class_id < len(class_names):
                            class_name = class_names[class_id]
                            print(f"Class ID: {class_id}, Class Name: {class_name}")
                        else:
                            print(f"Error: Class ID {class_id} exceeds available class names. Skipping.")
                            continue 

                        img_height, img_width, _ = image.shape
                        x1 = int((x_center - bbox_width / 2) * img_width)
                        y1 = int((y_center - bbox_height / 2) * img_height)
                        x2 = int((x_center + bbox_width / 2) * img_width)
                        y2 = int((y_center + bbox_height / 2) * img_height)

                        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) 
                        label = f"Class {class_names[class_id]}"
                        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    except (ValueError, IndexError) as e:
                        print(f"Error processing line: {line.strip()}. Error: {e}")
                        continue

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            plt.figure(figsize=(10, 10))
            plt.imshow(image_rgb)
            plt.axis('off') 
            plt.title(image_filename)
            plt.show()


def visualize_random_images(image_folder, label_folder, class_names, num_images=10):
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

    sampled_files = random.sample(image_files, min(num_images, len(image_files)))

    for image_filename in sampled_files:
        image_path = os.path.join(image_folder, image_filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Unable to read image {image_filename}. Skipping.")
            continue

        label_filename = image_filename.replace('.jpg', '.txt').replace('.png', '.txt')
        label_path = os.path.join(label_folder, label_filename)

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            for line in lines: 
                values = line.strip().split()  
                print(values)
                try:
                    class_id = int(values[0])  
                    x_center, y_center, bbox_width, bbox_height = map(float, values[1:5])  
                    
                    if class_id < len(class_names):
                        class_name = class_names[class_id]
                        print(f"Class ID: {class_id}, Class Name: {class_name}")
                    else:
                        print(f"Error: Class ID {class_id} exceeds available class names. Skipping.")
                        continue

                    img_height, img_width, _ = image.shape
                    x1 = int((x_center - bbox_width / 2) * img_width)
                    y1 = int((y_center - bbox_height / 2) * img_height)
                    x2 = int((x_center + bbox_width / 2) * img_width)
                    y2 = int((y_center + bbox_height / 2) * img_height)

                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) 
                    label = f"Class {class_names[class_id]}"
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                except (ValueError, IndexError) as e:
                    print(f"Error processing line: {line.strip()}. Error: {e}")
                    continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(10, 10))
        plt.imshow(image_rgb)
        plt.axis('off') 
        plt.title(image_filename)
        plt.show()

# import supervision as sv
# from ultralytics import YOLO
# import numpy as np
# # 1. Load model
# model = YOLO("runs_v2/detect/train/weights/best.pt")
# model.to(device)
# # 2. Load dataset 
# dataset = sv.DetectionDataset.from_yolo(
#     images_directory_path=r"c:\Users\Admin\Downloads\merged_dataset_v2_remove_dup\merged_dataset_v2_remove_dup\test\images",
#     annotations_directory_path=r"c:\Users\Admin\Downloads\merged_dataset_v2_remove_dup\merged_dataset_v2_remove_dup\test\labels",
#     data_yaml_path="merged_dataset_v3/data.yaml"
# )

# # 3. Định nghĩa callback function để chạy inference
# def callback(image: np.ndarray) -> sv.Detections:
#     # Chạy model prediction
#     result = model(image)[0]
#     # Chuyển đổi kết quả sang format của supervision
#     return sv.Detections.from_ultralytics(result)

# # 4. Tạo và tính toán confusion matrix
# confusion_matrix = sv.ConfusionMatrix.benchmark(
#     dataset=dataset,
#     callback=callback,
#     conf_threshold=0.25,  # có thể điều chỉnh ngưỡng confidence
#     iou_threshold=0.5  # có thể điều chỉnh ngưỡng IoU
# )

# # 5. Vẽ confusion matrix
# confusion_matrix.plot(
#     save_path="confusion_matrix.png",  # đường dẫn lưu ảnh
#     # class_names=dataset.classes  # tên các class
#     normalize=True, 
#     fig_size=(12, 10)
# )

# # 6. In các metrics
# print("Matrix:\n", confusion_matrix.matrix)  # In ma trận
# if hasattr(confusion_matrix, 'f1_scores'):
#     print("\nF1 scores per class:", confusion_matrix.f1_scores)  # In điểm F1
# if hasattr(confusion_matrix, 'map'):
#     print("mAP:", confusion_matrix.map)

visualize_random_images('data_aug/images', 'data_aug/labels', class_names)