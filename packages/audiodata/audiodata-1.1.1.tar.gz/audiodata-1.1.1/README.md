# Audio Metadata Extractor

This script extracts metadata from audio files using `pydub` and `mutagen` libraries with customised and fine-tuned outputs.

## Installation

To use this script, you need to have Python installed on your system. You can install the required dependencies using pip:

```
pip install pydub mutagen
```

## Usage

```
from audiodata import metadata

file_path = "path/to/audio.extension"
length_seconds, metadata = metadata.get_audio_metadata(file_path)

print(f"Audio Length: {length_seconds} seconds")
print("Metadata: \n" + metadata)
```

## Sample Output

```
Example:
----------------
Audio Length: 26.006 seconds
Metadata: 
tracknumber: 9, title: Komplexe Zahl, album: Funktionentheorie, artist: Engelbert Niehaus
```

## Support

If you find this script helpful, please do consider supporting the developer at [GitHub Sponsors](https://github.com/sponsors/Shreyan1)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt) file for details.

## Issues

Have any suggestions for imptovement ? Open an issue here - "https://github.com/Shreyan1/WhisperMe-Audio-Transcriber/issues"