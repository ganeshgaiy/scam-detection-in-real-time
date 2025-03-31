import os
import librosa
import soundfile as sf
import numpy as np
import random

# Directory paths
normal_call_dir = 'output_normal_left_cleaned'  # Input folder of cleaned normal calls
segmented_dir = 'output_normal_left_segmented'  # Output folder for segmented clips

# Create the output directory if it doesn't exist
if not os.path.exists(segmented_dir):
    os.makedirs(segmented_dir)

# Parameters for segment lengths
min_segment_length = 5  # in seconds
max_segment_length = 30  # in seconds

def segment_normal_calls(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            filepath = os.path.join(directory, filename)
            
            # Load the audio file
            y, sr = librosa.load(filepath, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            
            start = 0  # starting point of each segment
            segment_count = 1  # track segment number

            while start < duration:
                # Random segment length within the specified range
                segment_length = random.uniform(min_segment_length, max_segment_length)
                
                # Ensure the segment doesn't exceed the audio duration
                end = min(start + segment_length, duration)
                
                # Extract the segment
                y_segment = y[int(start * sr):int(end * sr)]
                
                # Define output filename and save the segment
                output_filename = f"{filename[:-4]}_segment_{segment_count}.wav"
                output_path = os.path.join(segmented_dir, output_filename)
                sf.write(output_path, y_segment, sr)
                
                # Update start position and segment count
                start = end
                segment_count += 1

            print(f"Segmented {filename} into {segment_count - 1} segments")

# Run the segmentation function
segment_normal_calls(normal_call_dir)
