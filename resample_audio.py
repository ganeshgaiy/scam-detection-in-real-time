from pydub import AudioSegment
import os

# Function to check if the audio file is stereo
def is_stereo(file):
    try:
        audio = AudioSegment.from_file(file, format="wav")
        return audio.channels == 2
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return False

# Function to get the sample rate of an audio file
def get_sample_rate(file):
    try:
        audio = AudioSegment.from_file(file, format="wav")
        return audio.frame_rate
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return None

# Function to change the sample rate of an audio file (optional)
def change_sample_rate(file, output_folder):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file, format="wav")
        # Resample the audio to 16000 Hz
        audio_16k = audio.set_frame_rate(16000)
        # Get the original file name
        file_name = os.path.basename(file)
        # Save the output file with the same name in the output folder
        output_path = os.path.join(output_folder, file_name)
        audio_16k.export(output_path, format="wav")
        print(f"Resampled file saved to: {output_path}")
    except Exception as e:
        print(f"Error changing sample rate for {file}: {e}")

# Function to separate left and right channels and save them as mono files
def separate_channels(file, left_output_folder, right_output_folder):
    try:
        # Load the audio file
        audio = AudioSegment.from_file(file, format="wav")
        # Split the audio into left and right channels
        left_channel = audio.split_to_mono()[0]
        right_channel = audio.split_to_mono()[1]
        
        # Get the original file name without the extension
        file_name = os.path.basename(file).split('.')[0]

        # Save the left and right channels as separate files in respective folders
        left_output_path = os.path.join(left_output_folder, f"{file_name}_left.wav")
        right_output_path = os.path.join(right_output_folder, f"{file_name}_right.wav")
        
        left_channel.export(left_output_path, format="wav")
        right_channel.export(right_output_path, format="wav")
        
        print(f"Left channel saved to: {left_output_path}")
        print(f"Right channel saved to: {right_output_path}")
    except Exception as e:
        print(f"Error separating channels for {file}: {e}")

# Define the folder paths
folder_path = "./audio-files/stereo"
left_output_folder = "./audio-files/output_left"   # Folder for left channel files
right_output_folder = "./audio-files/output_right" # Folder for right channel files

# Ensure the output folders exist
if not os.path.exists(left_output_folder):
    os.makedirs(left_output_folder)
if not os.path.exists(right_output_folder):
    os.makedirs(right_output_folder)

# Process each file in the folder
for i in os.listdir(folder_path):
    file_path = os.path.join(folder_path, i)
    if os.path.isfile(file_path):
        # Check if the file is stereo
        if is_stereo(file_path):
            print(f"{i} is a stereo file.")
            print(f"Original sample rate: {get_sample_rate(file_path)} Hz for file {i}")
            # Separate the left and right channels into respective folders
            separate_channels(file_path, left_output_folder, right_output_folder)
        else:
            print(f"{i} is not a stereo file. Skipping channel separation.")
