import os
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Define directories for robocall and normal call audio files
robocall_dir = './robocall_left'  # Replace with the actual path
normal_call_dir = 'output_normal_left_cleaned'  # Replace with the actual path

# Function to calculate durations of audio files in a directory
def calculate_durations(directory):
    durations = []
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            filepath = os.path.join(directory, filename)
            
            # Check if the file exists and handle errors
            if not os.path.isfile(filepath):
                print(f"File not found: {filepath}")
                continue

            try:
                y, sr = librosa.load(filepath, sr=None)  # Load with original sampling rate
                duration = librosa.get_duration(y=y, sr=sr)
                durations.append(duration)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    return durations

# Calculate durations for both directories
robocall_durations = calculate_durations(robocall_dir)
normal_call_durations = calculate_durations(normal_call_dir)

# Function to print and plot duration statistics
def display_statistics(durations, label):
    # Calculate statistics
    mean_duration = np.mean(durations)
    median_duration = np.median(durations)
    min_duration = np.min(durations)
    max_duration = np.max(durations)

    # Display statistics
    print(f"--- {label} ---")
    print(f"Mean Duration: {mean_duration:.2f} seconds")
    print(f"Median Duration: {median_duration:.2f} seconds")
    print(f"Minimum Duration: {min_duration:.2f} seconds")
    print(f"Maximum Duration: {max_duration:.2f} seconds")

    # Plot histogram
    plt.hist(durations, bins=20, alpha=0.6, color='b')
    plt.title(f"{label} Duration Distribution")
    plt.xlabel("Duration (seconds)")
    plt.ylabel("Frequency")
    plt.show()

# Display statistics for robocall and normal call durations
display_statistics(robocall_durations, "Robocall")
display_statistics(normal_call_durations, "Normal Call")
