import os

# Hàm chuyển đổi 8 giá trị tọa độ góc (x1, y1, x2, y2, x3, y3, x4, y4) về YOLO format (x_center, y_center, width, height)
def convert_to_yolo_format(coords):
    x_coords = [coords[0], coords[2], coords[4], coords[6]]
    y_coords = [coords[1], coords[3], coords[5], coords[7]]
    
    # Tìm x_min, x_max, y_min, y_max từ tọa độ của các điểm
    x_min = min(x_coords)
    x_max = max(x_coords)
    y_min = min(y_coords)
    y_max = max(y_coords)
    
    # Tính toán x_center, y_center, width, height
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    # Đảm bảo x_center, y_center, width, height nằm trong khoảng [0, 1]
    x_center = max(min(x_center, 1.0), 0.0)
    y_center = max(min(y_center, 1.0), 0.0)
    width = max(min(width, 1.0), 0.0)
    height = max(min(height, 1.0), 0.0)
    
    return [x_center, y_center, width, height]

# Hàm xử lý file nhãn
def process_label_file(label_file):
    cleaned_lines = []
    
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        values = list(map(float, line.strip().split()))
        
        if len(values) > 13:  # Kiểm tra xem có ít nhất 13 giá trị
            class_id = int(values[0])  # Class ID là giá trị đầu tiên
            coords = values[6:14]  # Lấy 8 giá trị (x1, y1, x2, y2, x3, y3, x4, y4) từ vị trí thứ 6
            if len(coords) == 8: 
                # Chuyển đổi về YOLO format
                yolo_bbox = convert_to_yolo_format(coords)
                # Thêm class ID và bounding box vào danh sách kết quả
                cleaned_lines.append(f'{class_id} ' + ' '.join(map(str, yolo_bbox)) + '\n')
            else:
                cleaned_lines.append(line)  # Nếu không đủ 8 giá trị, giữ nguyên dòng
        else:
            cleaned_lines.append(line)  # Nếu không đủ giá trị, giữ nguyên dòng
    
    # Ghi lại file sau khi xử lý
    with open(label_file, 'w') as f:
        f.writelines(cleaned_lines)

# Hàm xử lý tất cả các file trong thư mục
def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            process_label_file(file_path)
            print(f'Processed {filename}')

# Đường dẫn tới thư mục chứa file nhãn
folder_path = 'datatest/train/labels'

# Bắt đầu xử lý
process_folder(folder_path)
