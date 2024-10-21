import os
import shutil
from tqdm import tqdm

def merge_datasets(dataset1_path, dataset2_path, output_path, classes_to_remove):
    """Merge two datasets with different number of classes and remove unwanted classes."""
    
    # Create output directories if they don't exist
    os.makedirs(os.path.join(output_path, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_path, 'labels'), exist_ok=True)
    
    # Get all unique classes from both datasets
    classes = set()
    for dataset_path in [dataset1_path, dataset2_path]:
        with open(os.path.join(dataset_path, 'classes.txt'), 'r') as f:
            classes.update(f.read().splitlines())
    
    # Remove unwanted classes
    classes = classes - set(classes_to_remove)
    
    # Create a new class mapping
    class_mapping = {cls: idx for idx, cls in enumerate(sorted(classes))}
    
    # Write new classes file
    with open(os.path.join(output_path, 'classes.txt'), 'w') as f:
        for cls in sorted(classes):
            f.write(f"{cls}\n")
    
    # Process each dataset
    for dataset_path in [dataset1_path, dataset2_path]:
        # Load original class mapping
        original_classes = {}
        with open(os.path.join(dataset_path, 'classes.txt'), 'r') as f:
            original_classes = {idx: cls for idx, cls in enumerate(f.read().splitlines())}
        
        # Process images and labels
        image_folder = os.path.join(dataset_path, 'images')
        label_folder = os.path.join(dataset_path, 'labels')
        
        for filename in tqdm(os.listdir(image_folder), desc=f"Processing {os.path.basename(dataset_path)}"):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Process label
                label_filename = os.path.splitext(filename)[0] + '.txt'
                label_path = os.path.join(label_folder, label_filename)
                if os.path.exists(label_path):
                    with open(label_path, 'r') as f:
                        lines = f.readlines()
                    
                    # Update class IDs and remove unwanted classes
                    updated_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        old_class_id = int(parts[0])
                        old_class_name = original_classes[old_class_id]
                        if old_class_name not in classes_to_remove:
                            new_class_id = class_mapping[old_class_name]
                            updated_lines.append(f"{new_class_id} {' '.join(parts[1:])}\n")
                    
                    # Only copy image and write label if there are any objects left after removing unwanted classes
                    if updated_lines:
                        # Copy image
                        shutil.copy2(
                            os.path.join(image_folder, filename),
                            os.path.join(output_path, 'images', filename)
                        )
                        
                        # Write updated label
                        with open(os.path.join(output_path, 'labels', label_filename), 'w') as f:
                            f.writelines(updated_lines)

# Paths to your datasets and output
dataset1_path = r'C:\Users\Admin\Downloads\hazardous_tem_craw.v2i.yolov11'
dataset2_path = 'merged_dataset'
output_path = 'merged_dataset_v2'

# List of classes to remove
classes_to_remove = ['008_Inhalation hazard', '016_BlueBarrel']

# Merge datasets
merge_datasets(dataset1_path, dataset2_path, output_path, classes_to_remove)

# Count files in the merged dataset
image_count = len([f for f in os.listdir(os.path.join(output_path, 'images')) if f.endswith(('.jpg', '.jpeg', '.png'))])
label_count = len([f for f in os.listdir(os.path.join(output_path, 'labels')) if f.endswith('.txt')])

print(f'Total images in merged dataset: {image_count}')
print(f'Total labels in merged dataset: {label_count}')