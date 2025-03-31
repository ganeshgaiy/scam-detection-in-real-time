import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Define your directories
input_folder = './output_left_normal'
output_folder = 'output_normal_left_cleaned'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Silence removal settings
min_silence_len = 500  # Minimum length of silence to detect (in ms)
silence_thresh = -40  # Silence threshold (in dB)
padding_duration = 200  # Add a bit of silence (in ms) to smooth transitions

# Process each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.wav'):
        # Load audio file
        audio_path = os.path.join(input_folder, filename)
        audio = AudioSegment.from_wav(audio_path)
        
        # Split on silence and retain non-silent parts
        chunks = split_on_silence(audio,
                                  min_silence_len=min_silence_len,
                                  silence_thresh=silence_thresh,
                                  keep_silence=padding_duration)
        
        # Concatenate all chunks to form a continuous stream
        cleaned_audio = AudioSegment.empty()
        for chunk in chunks:
            cleaned_audio += chunk
        
        # Export cleaned audio
        output_path = os.path.join(output_folder, filename)
        cleaned_audio.export(output_path, format='wav')
        print(f"Processed and saved: {output_path}")

print("Silence removal complete for all files in the folder.")
