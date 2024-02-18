'''
Created by Shreyan Basu Ray [Github - https://github.com/Shreyan1] @2024
Support me at - https://github.com/sponsors/Shreyan1

Sample Usage : 
-----------------
from audiodata import metadata

file_path = "path/to/audio.extension"
length_seconds, metadata = metadata.get_audio_metadata(file_path)

print(f"Audio Length: {length_seconds} seconds")
print("Metadata: \n" + metadata)

Sample Output
-----------------

Audio Length: 26.006 seconds
Metadata: 
tracknumber: 9, title: Komplexe Zahl, album: Funktionentheorie, artist: Engelbert Niehaus

'''

from pydub import AudioSegment
from mutagen import File
import os

def get_audio_metadata(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        return "File does not exist", ""

    try:
        # Get audio length
        audio = AudioSegment.from_file(file_path)
        length_seconds = len(audio) / 1000
        
    except Exception as e:
        return f"Error processing audio length: {e}", ""

    try:
        # Get metadata with mutagen
        # Using easy=True to simplify metadata, otherwise album would come as TALB, date as TDRC, etc
        #TCON: Death Metal TDRC: 2024 TALB: WhisperMe TIT2: SpeechTest TPE1: Shreyan
        audio_file = File(file_path, easy=True)
        metadata = audio_file.tags if audio_file else {}
        
    except Exception as e:
        return length_seconds, f"Error extracting metadata: {e}"

    # Format metadata
    metadata_str = ""
    #Check if metadata is not empty and apply format
    if metadata:
        metadata_items = [f"{key}: {', '.join(value) if isinstance(value, list) else value}" for key, value in metadata.items()]
        metadata_str = ', '.join(metadata_items)

    return length_seconds, metadata_str.strip()

