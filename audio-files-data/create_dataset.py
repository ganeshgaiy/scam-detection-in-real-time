import os
import random
import shutil

# Define directories
segmented_normal_dir = 'output_normal_left_segmented'
robocall_dir = 'robocall_left'
dataset_dir = 'dataset'

# Create dataset structure
os.makedirs(os.path.join(dataset_dir, 'robocall'), exist_ok=True)
os.makedirs(os.path.join(dataset_dir, 'normal_call'), exist_ok=True)

# Copy all robocall files to the dataset
for file in os.listdir(robocall_dir):
    if file.endswith('.wav'):
        try:
            shutil.copy(os.path.join(robocall_dir, file), os.path.join(dataset_dir, 'robocall', file))
        except FileNotFoundError as e:
            print(f"Error copying file {file}: {e}")

# Select 1000 random segmented normal call files
normal_files = [file for file in os.listdir(segmented_normal_dir) if file.endswith('.wav')]

# Check if there are enough files
if len(normal_files) < 1000:
    print("Not enough files in segmented_normal_dir to sample 1000.")
else:
    selected_normal_files = random.sample(normal_files, 1000)

    # Copy selected normal call files to the dataset
    for file in selected_normal_files:
        try:
            shutil.copy(os.path.join(segmented_normal_dir, file), os.path.join(dataset_dir, 'normal_call', file))
        except FileNotFoundError as e:
            print(f"Error copying file {file}: {e}")

print("Dataset creation complete with balanced classes.")
