import os
import cv2

# Đường dẫn đến thư mục chứa ảnh và file nhãn
image_folder = 'data_aug/train/images'  # Thư mục chứa ảnh
label_folder = 'data_aug/train/labels'  # Thư mục chứa nhãn

class_name_mapping = {
    '1 Explosives': 0,
    '1-1 Explosives Products with the potential to create a mass explosion': 1,
    '1-2 Explosives Products with the potential to create a projectile hazard': 2,
    '1-3 Explosives Products with the potential to create a fire or minor blast': 3,
    '1-4 Explosives Products with no significant risk of creating a blast': 4,
    '1-5 Explosives Products considered very insensitive that are used as blasting agents': 5,
    '1-6 Explosives Products considered extremely insensitive with no risk to create a mass explosion': 6,
    '2 Oxygen': 7,
    '2-1 Flammable gases': 8,
    '2-2 Nonflammable gases': 9,
    '2-3 Toxic gases': 10,
    '3 Combustible': 11,
    '3 Flammable': 12,
    '3 Flammable and combustible liquids': 13,
    '3 Flammable liquid': 14,
    '4-1 Flammable solids': 15,
    '4-2 Spontaneously combustible': 16,
    '4-3 Dangerous when wet': 17,
    '5-1 Oxidizing substances': 18,
    '5-2 Organic peroxides': 19,
    '6 Poisons': 20,
    '7 Radioactive': 21,
    '8 Corrosive': 22,
    '9 Miscellaneous': 23,
    'Dangerous': 24,
    'Environmentally Hazardous Substance': 25,
    'Hot': 26,
    'Infectious Substance': 27,
    'Orange Panel': 28,
    'Placards': 29,
    'Spontaneously combustible material': 30,
    'license plate': 31
}

# Lặp qua từng file ảnh trong thư mục
for image_filename in os.listdir(image_folder):
    if image_filename.endswith('.jpg') or image_filename.endswith('.png'):
        # Đọc ảnh
        image_path = os.path.join(image_folder, image_filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Unable to read image {image_filename}. Skipping.")
            continue  # Bỏ qua ảnh nếu không đọc được

        # Đọc file nhãn tương ứng
        label_filename = image_filename.replace('.jpg', '.txt').replace('.png', '.txt')
        label_path = os.path.join(label_folder, label_filename)

        # Đọc các bounding box từ file nhãn
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                values = line.strip().split()[:5]  # Chỉ lấy 5 giá trị đầu tiên
                
                # Lấy class_id từ mapping
                class_name = values[0]
                class_id = class_name_mapping.get(class_name)
                if class_id is None:
                    print(f"Warning: Class '{class_name}' not found in mapping. Skipping.")
                    continue  # Bỏ qua nếu không tìm thấy class_id

                try:
                    # Chuyển đổi còn lại sang float
                    x_center, y_center, bbox_width, bbox_height = map(float, values[1:5])
                except ValueError as e:
                    print(f"Error converting bounding box values: {e}. Skipping line: {line.strip()}")
                    continue

                # Tính toán tọa độ của bounding box
                img_height, img_width, _ = image.shape
                x1 = int((x_center - bbox_width / 2) * img_width)
                y1 = int((y_center - bbox_height / 2) * img_height)
                x2 = int((x_center + bbox_width / 2) * img_width)
                y2 = int((y_center + bbox_height / 2) * img_height)

                # Vẽ bounding box lên ảnh
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Màu đỏ
                label = f"Class {class_id}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Hiển thị ảnh
        cv2.imshow('Image with Labels', image)
        if cv2.waitKey(0) & 0xFF == ord('q'):  # Nhấn 'q' để thoát
            break

cv2.destroyAllWindows()
