# Video-Timestamper

## What Does it Do?
Video-Timestamper allows MOD and MP4 files saved in a given input directory to be timestamped based on their date 
modified timestamp. The videos will always be outputted to MP4 files to the given output directory. The slowest ffmpeg
setting is used to get the smallest MP4 files. Of course, more video file formats can be easily supported if desired.

## How 2 use Script?
You can either...

1. Run the Python script: `python -m video_timestamper -input_path "path/2/input/videos" -output_path "path/2/output/dir"`


2. Run the executable: `.\video_timestamper.exe -input_path "path/2/input/videos" -output+path "path/2/output/dir"`

Both `"path/2/input/videos"` and `"path/2/output/dir` can be an absolute path or a path relative to the Python script 
or executable. Either way, they must point to a directory that contains the videos that should be timestamped and the 
directory that will contain the timestamped videos, respectively. This directory will be created if it does not already 
exist.

Building a Windows executable can be done by running the build.bat script or the "build executable" configuration. 
Executables for other platforms can be built using a very similar method that was used to build the Windows executable.
However, this is not done here.

## How 2 Develop?
You will need:

- [PyCharm IDE](https://www.jetbrains.com/pycharm/download/) >= 2022.1 (recommended, but not necessary).

- [Python](https://www.python.org/downloads/) >= 3.10.

- [moviepy](https://pypi.org/project/moviepy/) >= 1.0.3 to extract the audio of the video for later merging.

- [opencv-python](https://pypi.org/project/opencv-python/) >= 4.5.5.64 to timestamp the videos.

- [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) >= 0.2.0 to merge the timestamped video with its audio.

- [tqdm](https://pypi.org/project/tqdm/) >= 4.64.0 to display the loading bars.

- [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/) >= 4.10 to build executable.
  - [UPX](https://upx.github.io/) >= 3.96 if you would like to make smaller executables.