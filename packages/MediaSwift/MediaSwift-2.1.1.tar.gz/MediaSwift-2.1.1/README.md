## [MediaSwift] - EMPOWERING PYTHON WITH ADVANCED MULTIMEDIA OPERATIONS.

#### A POWERFUL PYTHON LIBRARY FOR SEAMLESS MULTIMEDIA OPERATIONS. MediaSwift SIMPLIFIES COMPLEX TASKS, MAKING IT EASY TO INTEGRATE AND ENHANCE YOUR MULTIMEDIA APPLICATIONS. DIVE INTO THE FUTURE OF MEDIA HANDLING WITH MediaSwift - YOUR GO-TO LIBRARY FOR 2024.

**KEY FEATURES:**
- **EFFORTLESS FILE CONVERSION .**
- **SEAMLESS MULTIMEDIA PLAYBACK .**
- **PROVIDING INFORMATION:**
  **MediaSwift ALSO OFFERS DETAILED MULTIMEDIA INFORMATION RETRIEVAL .**


### EXPLORE THE CAPABILITIES OF MediaSwift AND ELEVATE YOUR PYTHON MULTIMEDIA PROJECTS WITH SIMPLICITY AND EFFICIENCY.


[![License](https://img.shields.io/badge/LICENSE-GPLv3-blue.svg)](https://github.com/yourusername/MediaSwift/blob/main/LICENSE)

**[MediaSwift]**: **IS A PYTHON LIBRARY THAT PROVIDES A SIMPLIFIED INTERFACE FOR USING MediaSwift AND FFPROBE, ALLOWING USERS TO PERFORM VIDEO CONVERSION AND PROBING WITH EASE.**

### Video Codecs: `h264`, `libx264`, `mpeg4`, `vp9`, `av1`, `hevc`, `mjpeg`, `H.265 / HEVC`, `VP8`, `VP9`, `AV1`, `VC1`, `MPEG1`, `MPEG2`, `H.263`, `Theora`, `MJPEG`, `MPEG-3`,`MPEG-4`, '-more'.
### Audio Codecs: `aac`, `mp3`, `opus`, `vorbis`, `pcm`, `alac`, `flac`, `wv`, `ape`, `mka`, `opus`, `ac3`, `eac3`, `alac`, '-more'.
### Supported File Extensions: Video Formats - `.mp4`, `.avi`, `.mkv`, `.webm`, `.mov`, `.wmv`, `.webm`, `.flv`, `.mov`, `.wmv`, `.hevc`, `.prores`, `.dv`; Audio Formats - `.mp3`, `.aac`, `.ogg`, `.wav`, `.flac`, `.flac`, `.m4a`, `.ogg`, `.wv`, `.ape`, `.mka`, `.opus`, `mpc`, `.tak`, `.alac` '-more'.

**NOTE: ALSO SUPPORT DOLBY DIGITAL PLUS AUDIO CODEC `.eac3`
AND SUPPORT MORE VIDEO AND AUDIO CODECS AND VARIOUS [FORMATE EXTENSION].**

**[MediaSwift]: A VERSATILE LIBRARY WITH MANY SUPPORT FOR AUDIO AND VIDEO CODECS, AS WELL AS MULTIPLE FILE FORMATS.**


## - LIST THE AVAILABLE CODECS AND FORMATES:

`ffmpe = ffpe()`

- `ffmpe.formats()`
- `ffmpe.codecs()`

#### USE `.formate()` AND `.codecs()` METHOD.

## - CHECK LIBRARY VERSION USING:

```python
from MediaSwift import version

version = version()
print(version)
```

## - PLAY MEDIA USING FFPL
#### THE `ffpl` CLASS PROVIDES METHODS FOR PLAY MEDIA FILES. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS:

```python
from MediaSwift import ffpl

play = ffpl()
media_file = r"PATH_TO_INPUT_FILE"
play.play(media_file)
```

#### USE THE `.play()` METHOD TO PLAY MEDIA.

## - Using the `ffpr` class

#### THE `ffpr` CLASS PROVIDES METHODS FOR PROBING MEDIA FILES. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS:

```python
from MediaSwift import ffpr

ffprobe = ffpr()

info = ffprobe.probe(r"PATH_TO_INPUT_FILE")
ffprobe.pretty(info)
```

#### IN THIS EXAMPLE, REPLACE `"PATH_TO_MEDIA_FILE"` WITH THE ACTUAL PATH TO YOUR MEDIA FILE. THE `.probe` METHOD RETURNS A DICTIONARY CONTAINING INFORMATION ABOUT THE MEDIA FILE. THE `.pretty`

## - USING THE `FFPE` CLASS

#### THE `FFPE` CLASS PROVIDES METHODS FOR VIDEO CONVERSION, LISTING CODECS, AND LISTING FORMATS. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS:

#### - EXAMPLE - CONVERT SINGLE VIDEO USING THIS: 
```python
from MediaSwift import ffpe

ffmpe = ffpe()

ffmpe.convert(
    input_files=[r"PATH_TO_INPUT_FILE"],
    output_dir=r"PATH_TO_OUTPUT_FILE",
    cv='h264',        # VIDEO CODEC
    ca='aac',         # AUDIO CODEC
    s='1920x1080',    # VIDEO RESOLUTION
    hwaccel='cuda',   # HARDWARE ACCELERATION
    ar=44100,         # AUDIO SAMPLE RATE
    ac=2,             # AUDIO CHANNELS
    ba=192000,        # AUDIO BITRATE
    r=30,             # VIDEO FRAME RATE
    f='mp4',          # OUTPUT FORMAT
    preset='fast',    # PRESET FOR ENCODING
    bv=2000           # VIDEO BITRATE
)
```
#### - EXAMPEL - CONVERT MULTIPLE VIDEO USING THIS: 
- NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS: 
```python
from MediaSwift import ffpe

ffpe_instance = ffpe()

input_files = [
    r"PATH_TO_INPUT_FILE",
    r"PATH_TO_INPUT_FILE",
    # ADD MORE FILE PATHS AS NEEDED
]
output_directory = r"PATH_TO_OUTPUT_FILE"

ffpe_instance.convert_with_threading(
    file_list=input_files,
    output_dir=output_directory,
    cv="libx264",     # VIDEO CODEC
    ca="aac",         # AUDIO CODEC
    s="1280x720",     # VIDEO RESOLUTION
    ar=44100,         # AUDIO SAMPLE RATE
    ac=2,             # AUDIO CHANNELS 
    ba=128000,        # AUDIO BITRATE 
    r=30,             # VIDEO FRAME RATE 
    f="avi",          # OUTPUT FORMAT 
    preset="medium",  # PRESET FOR ENCODING 
    bv=1000000,       # VIDEO BITRATE 
)
```
#### - USE THE `.convert()` METHOD TO CONVERT MEDIA.
- NOTE - ALWAYS SET INPUT FILE PATH IN SQUARE BRACKETS: 


## - IMPORT CLASS:

- `from MediaSwift import ffpe, ffpl, ffpr`
- `from MediaSwift import *`

## - INSTALLATION:

```bash
pip install MediaSwift
```
##  CONTACT
```
THIS PROJECT IS MAINTAINED BY [ROHIT SINGH]. FOR ANY QUERIES OR CONTRIBUTIONS TO CHECK MY GITHUB, PLEASE REACH OUT TO US. THANK YOU FOR USING 'MediaSwift' PYTHON LIBRARY, NEW LIBRARY 2024.
```
