import os

# Hàm để chuyển từ tọa độ sang định dạng YOLO (4 giá trị)
def convert_to_yolo_format(coords):
    x_coords = [coords[0], coords[2], coords[4], coords[6]]
    y_coords = [coords[1], coords[3], coords[5], coords[7]]
    
    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)
    
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    # Đảm bảo các giá trị nằm trong phạm vi [0.0, 1.0]
    x_center = max(min(x_center, 1.0), 0.0)
    y_center = max(min(y_center, 1.0), 0.0)
    width = max(min(width, 1.0), 0.0)
    height = max(min(height, 1.0), 0.0)
    
    return [x_center, y_center, width, height]

# Hàm để kiểm tra file label và chuyển đổi nếu cần
def process_label_file(label_file):
    cleaned_lines = []
    
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        values = list(map(float, line.strip().split()))
        
        # Nếu số lượng giá trị > 5
        if len(values) > 5:
            class_id = int(values[0])  # Lấy class_id
            # Lấy tối đa 8 giá trị tọa độ để chuyển đổi
            coords = values[1:9] if len(values) >= 9 else values[1:]
            if len(coords) == 8:  # Chỉ thực hiện nếu có đủ 8 giá trị
                yolo_bbox = convert_to_yolo_format(coords)
                cleaned_lines.append(f'{class_id} ' + ' '.join(map(str, yolo_bbox)) + '\n')
            else:
                cleaned_lines.append(line)  # Giữ nguyên nếu không đủ 8 giá trị
        else:
            cleaned_lines.append(line)  # Giữ nguyên nếu chỉ có 5 giá trị

    # Ghi lại dữ liệu đã được làm sạch vào file
    with open(label_file, 'w') as f:
        f.writelines(cleaned_lines)

# Hàm để lặp qua tất cả các file trong thư mục và xử lý
def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            process_label_file(file_path)
            print(f'Processed {filename}')

# Đường dẫn tới thư mục chứa file .txt
folder_path = 'Hazmat Placards.v1i.yolov11/train/labels'

# Gọi hàm xử lý thư mục
process_folder(folder_path)
