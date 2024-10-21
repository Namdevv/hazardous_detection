import os
from tqdm import tqdm

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

    x_center = max(min(x_center, 1.0), 0.0)
    y_center = max(min(y_center, 1.0), 0.0)
    width = max(min(width, 1.0), 0.0)
    height = max(min(height, 1.0), 0.0)
    
    return [x_center, y_center, width, height]

def process_label_file(label_file):
    cleaned_lines = []
    
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        values = list(map(float, line.strip().split()))
        
        if len(values) > 13:  
            class_id = int(values[0])  
            coords = values[6:14] 
            if len(coords) == 8: 
                yolo_bbox = convert_to_yolo_format(coords)
                cleaned_lines.append(f'{class_id} ' + ' '.join(map(str, yolo_bbox)) + '\n')
            else:
                cleaned_lines.append(line)  
        else:
            cleaned_lines.append(line) 
    
    with open(label_file, 'w') as f:
        f.writelines(cleaned_lines)

def process_folder(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    for filename in tqdm(txt_files, desc="Processing files"):
        file_path = os.path.join(folder_path, filename)
        process_label_file(file_path)


folder_path = 'Hazmat Placards.v3i.yolov11/labels'

process_folder(folder_path)
