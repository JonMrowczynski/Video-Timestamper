# Video-Timestamper

## Backstory
During one of my side projects, I needed to convert a batch of MOD videos into MP4s. Additionally, I required local 
timestamps to be printed on the entire video indicating when each frame was taken.

There are some free, yet inconvenient cloud based options that would have required me to upload my videos to perform the 
conversion process, which would have taken quite some time (i.e. I am not going to upload tens if not hundreds of 
Gigabytes of data to some server to then have to download even more data later).

Alternatively there are downloadable programs that could perform this same conversion process, but they had constraints 
imposed on the conversions. For example, only three videos or only 5-minute videos, etc., can be converted before 
needing to pay, and why pay for something that you can make for free?

Either way, neither of these solutions would have been able to put the local timestamps on the video. In addition to 
placing timestamps on MOD files, I also required this function to be performed on MP4s. This solution allows for both
processes to be performed in one go.

It should be noted that this process can work on other video file formats. I just happened to have MOD and MP4 files
that required this processing.

## What Does it Do?
Video-Timestamper allows MOD and MP4 files saved in a given input directory to be timestamped based on their date 
modified timestamp. The videos will always be outputted as MP4 files to the given output directory. The slowest ffmpeg
setting is used to output the smallest MP4 files. It was very important for my purposes that the outputted videos took 
up the least amount of space. However, this setting can easily be modified to speed up the video processing, if desired.

## How 2 use Script?
You can either...

1. Run the Python script: `python -m video_timestamper -input_path "path/2/input/videos" -output_path "path/2/output/dir"`


2. Run the executable: `.\video_timestamper.exe -input_path "path/2/input/videos" -output+path "path/2/output/dir"`

Both `"path/2/input/videos"` and `"path/2/output/dir` can be an absolute path or a path relative to the Python script 
or executable. Either way, they must point to a directory that contains the videos that should be timestamped (and 
converted to MP4 if they are some other video format) and the directory that will contain the timestamped MP4 videos, 
respectively. This output directory will be created if it does not already exist.

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