import os
import hashlib
from tqdm import tqdm

def hash_image(image_path):
    """Generate a hash for the image file."""
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def remove_duplicates(image_folder, label_folder):
    seen_hashes = set()  
    images_to_delete = []  

    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for filename in tqdm(image_files, desc="Processing images", unit="image"):
        image_path = os.path.join(image_folder, filename)
        image_hash = hash_image(image_path)

        if image_hash in seen_hashes:
            images_to_delete.append(image_path)
            label_file = os.path.splitext(filename)[0] + '.txt'  
            label_path = os.path.join(label_folder, label_file)  
            
            if os.path.exists(label_path):
                images_to_delete.append(label_path)
        else:
            seen_hashes.add(image_hash)

    for file_path in tqdm(images_to_delete, desc="Deleting files", unit="file"):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f'Error deleting {file_path}: {e}')

image_folder = 'raw_data/total_image'
label_folder = 'raw_data/total_labels'

# remove_duplicates(image_folder, label_folder)


def count_files(folder_path):
    """Count the number of files in the specified folder."""
    return len(os.listdir(folder_path))

image_folder = 'raw_data/total_image'
label_folder = 'raw_data/total_labels'

image_count = count_files(image_folder)
label_count = count_files(label_folder)

print(f'Total images: {image_count}')
print(f'Total labels: {label_count}')

def check_images_without_labels(image_folder, label_folder):
    """Check for images that do not have corresponding label files."""
    images_without_labels = []  # List to store images without labels
    
    # Lấy danh sách tệp tin trong thư mục hình ảnh
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Kiểm tra từng tệp ảnh
    for filename in tqdm(image_files, desc="Checking images", unit="image"):
        label_file = os.path.splitext(filename)[0] + '.txt'  # Chỉ tên tệp, không phải đường dẫn đầy đủ
        label_path = os.path.join(label_folder, label_file)  # Tạo đường dẫn đầy đủ cho tệp nhãn
        
        if not os.path.exists(label_path):
            images_without_labels.append(filename)  # Thêm tên tệp ảnh vào danh sách nếu không có nhãn

    return images_without_labels  # Trả về danh sách ảnh không có nhãn

# Đường dẫn đến thư mục chứa ảnh và nhãn
image_folder = 'raw_data/total_image'
label_folder = 'raw_data/total_labels'

# Gọi hàm kiểm tra
images_without_labels = check_images_without_labels(image_folder, label_folder)