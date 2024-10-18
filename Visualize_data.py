import os
import cv2
import matplotlib.pyplot as plt
import random

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

