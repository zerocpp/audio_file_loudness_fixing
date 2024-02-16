import os
from pydub import AudioSegment
from pydub.playback import play
from tqdm import tqdm

def calculate_loudness(audio_file):
    audio = AudioSegment.from_file(audio_file)
    return audio.dBFS

def adjust_volume(audio_file, target_dBFS):
    audio = AudioSegment.from_file(audio_file)
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)

def process_folder(input_folder_path, export_folder_path):
    audio_files = [(f, os.path.join(input_folder_path, f), os.path.join(export_folder_path, f)) for f in os.listdir(input_folder_path) if f.endswith('.mp3')]

    loudness_values = []

    # Calculate the average loudness of each file
    for file_name, input_file, output_file in tqdm(audio_files):
        loudness = calculate_loudness(input_file)
        loudness_values.append(loudness)
        print(f'loudness:{loudness}  file:{file_name}')

    # Find the maximum average loudness
    max_loudness = max(loudness_values)
    print(f'max loudness:{max_loudness}')
    

    # Adjust the volume of each audio file to the max average loudness
    for file_name, input_file, output_file in tqdm(audio_files):
        louder_audio = adjust_volume(input_file, max_loudness)
        # Save the adjusted audio file, might overwrite the original or save as a new file
        louder_audio.export(output_file, format='mp3')


INPUT_FOLDER_PATH='F:/王玥波 水浒全传/'
OUTPUT_FOLDER_PATH='F:/王玥波-水浒全传（音量修复）/'
if not os.path.exists(OUTPUT_FOLDER_PATH):
    os.mkdir(OUTPUT_FOLDER_PATH)

# Replace 'your_folder_path' with the path to the folder containing your MP3 files
process_folder(input_folder_path=INPUT_FOLDER_PATH, export_folder_path=OUTPUT_FOLDER_PATH)
