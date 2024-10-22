import os
import hashlib
from tqdm import tqdm
from PIL import Image

def hash_image(image_path):
    """Generate a hash for the image file."""
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def is_image_too_small(image_path, min_size=(100, 100)):
    """Check if the image is smaller than the minimum size."""
    try:
        with Image.open(image_path) as img:
            return img.size[0] < min_size[0] or img.size[1] < min_size[1]
    except Exception as e:
        print(f"Error checking image size for {image_path}: {e}")
        return False

def remove_duplicates(image_folder, label_folder):
    seen_hashes = set()
    images_to_delete = []

    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    for filename in tqdm(image_files, desc="Processing images", unit="image"):
        image_path = os.path.join(image_folder, filename)
        
        if is_image_too_small(image_path):
            images_to_delete.append(image_path)
        else:
            image_hash = hash_image(image_path)
            if image_hash in seen_hashes:
                images_to_delete.append(image_path)
            else:
                seen_hashes.add(image_hash)

        label_file = os.path.splitext(filename)[0] + '.txt'
        label_path = os.path.join(label_folder, label_file)
        if os.path.exists(label_path) and image_path in images_to_delete:
            images_to_delete.append(label_path)

    for file_path in tqdm(images_to_delete, desc="Deleting files", unit="file"):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f'Error deleting {file_path}: {e}')


def count_files(folder_path):
    """Count the number of files in the specified folder."""
    return len(os.listdir(folder_path))


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


def sync_images_and_labels(image_folder, label_folder):
    """Synchronize images and labels, keeping only pairs that exist in both folders."""
    image_files = set(f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png')))
    label_files = set(f for f in os.listdir(label_folder) if f.endswith('.txt'))
    
    labels_to_delete = []
    for label_file in tqdm(label_files, desc="Checking labels", unit="file"):
        image_name = os.path.splitext(label_file)[0]
        if not any(image_name == os.path.splitext(img)[0] for img in image_files):
            labels_to_delete.append(os.path.join(label_folder, label_file))
    
    images_to_delete = []
    for image_file in tqdm(image_files, desc="Checking images", unit="file"):
        label_name = os.path.splitext(image_file)[0] + '.txt'
        if label_name not in label_files:
            images_to_delete.append(os.path.join(image_folder, image_file))
    
    # Delete orphaned files
    for file_path in tqdm(labels_to_delete + images_to_delete, desc="Deleting orphaned files", unit="file"):
        try:
            os.remove(file_path)
            print(f"Deleted orphaned file: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    print(f"Deleted {len(labels_to_delete)} orphaned label files and {len(images_to_delete)} orphaned image files.")

def main():
    image_folder = 'data_aug/images'
    label_folder = 'data_aug/labels'

    # remove_duplicates(image_folder, label_folder)
    # image_count = count_files(image_folder)
    # label_count = count_files(label_folder)
    # print(f'Total images after removing duplicates: {image_count}')
    # print(f'Total labels after removing duplicates: {label_count}')
    # images_without_labels = check_images_without_labels(image_folder, label_folder)
    # print(f'Total images without labels: {len(images_without_labels)}')
    sync_images_and_labels(image_folder, label_folder)

    image_count = len([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))])
    label_count = len([f for f in os.listdir(label_folder) if f.endswith('.txt')])

    print(f'Total images after synchronization: {image_count}')
    print(f'Total labels after synchronization: {label_count}')

if __name__ == "__main__":
    main()


