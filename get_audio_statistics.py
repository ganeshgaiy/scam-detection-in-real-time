import os
import glob
from pydub import AudioSegment
import matplotlib.pyplot as plt
from collections import Counter

# Define the folder path
folder_path = './audio-files-data/dataset/robocall'  # Replace with your folder path

# Collect all WAV files in the folder
audio_files = glob.glob(os.path.join(folder_path, '*.wav'))

# Count the number of audio files
num_files = len(audio_files)
print(f"Number of audio files: {num_files}")

# Initialize total duration and sample rates list
total_duration_ms = 0  # Total duration in milliseconds
sample_rates = []

# Process each audio file
for file in audio_files:
    try:
        audio = AudioSegment.from_wav(file)
        total_duration_ms += len(audio)  # Duration in milliseconds
        sample_rates.append(audio.frame_rate)
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Convert total duration to hours, minutes, seconds
total_duration_sec = total_duration_ms / 1000  # Convert to seconds
hours = int(total_duration_sec // 3600)
minutes = int((total_duration_sec % 3600) // 60)
seconds = int(total_duration_sec % 60)

print(f"Total duration: {hours} hours, {minutes} minutes, {seconds} seconds")

# Count the occurrences of each sample rate
sample_rate_counts = Counter(sample_rates)

# Extract sample rates and their counts
rates = list(sample_rate_counts.keys())
counts = list(sample_rate_counts.values())

# Sort the rates and counts for better visualization
sorted_rates_counts = sorted(zip(rates, counts))
sorted_rates, sorted_counts = zip(*sorted_rates_counts)

# Create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(sorted_rates, sorted_counts, color='skyblue')
plt.title('Distribution of Sample Rates')
plt.xlabel('Sample Rate (Hz)')
plt.ylabel('Number of Audio Files')
plt.xticks(sorted_rates)  # Ensure all sample rates are shown on the x-axis
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
