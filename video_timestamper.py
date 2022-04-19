"""
Copyright (c) 2022 Jon Mrowczynski

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This script timestamps videos in a given input directory and outputs the timestamped videos into a given output
directory as MP4s. The last modified timestamp of the video file is used as the end timestamp of the video since this
is when the video is written to file.
"""

from argparse import ArgumentParser
from datetime import datetime, timedelta
from os import remove, listdir
from os.path import basename, splitext, join
from pathlib import Path
from typing import Final

from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, \
    putText, FONT_HERSHEY_SIMPLEX, VideoWriter, VideoWriter_fourcc
from ffmpeg import input, concat
from moviepy.editor import AudioFileClip
from tqdm import tqdm

# The name of the temporary audio file that contains the audio from the original input video.
TEMP_AUDIO_FILE_NAME: Final = 'temp_audio.wav'

# The name of the temporary file that contains the timestamped MP4 video.
TEMP_TIMESTAMPED_VIDEO_FILE_NAME: Final = 'temp_timestamped_video.mp4'

# The format of the timestamp that is placed on each from of each video.
DATE_TIME_FORMAT: Final = '%Y-%m-%d %H:%M:%S'

# The amount that the timestamp should be offset from the bottom-right corner of each frame.
TEXT_OFFSET: Final = 50

# The color of the timestamp text.
WHITE: Final = (255, 255, 255)


def _extract_audio(video_path: str) -> None:
    """
    Extracts the audio from a video and writes it to a temporary WAV file.

    :param video_path: the path to the video whose audio is to be written to a temporary WAV file.
    """
    print('Extracting Audio...')
    with AudioFileClip(video_path) as audio:
        audio.write_audiofile(TEMP_AUDIO_FILE_NAME)
    print('Extracted Audio!')


def _timestamp_frames(video_path: str) -> None:
    """
    Adds timestamps to the video at video_path and saves the video as an MP4.

    :param video_path: the path to the video that will have timestamps added to the bottom-left corner of the screen.
    """
    print('Adding Timestamps to Video...')
    video = VideoCapture(video_path)
    fps, total_frames = video.get(CAP_PROP_FPS), int(video.get(CAP_PROP_FRAME_COUNT))
    w, h = int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT))
    writer = VideoWriter(TEMP_TIMESTAMPED_VIDEO_FILE_NAME, VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    with tqdm(total=total_frames, position=0, leave=False, dynamic_ncols=True) as pbar:
        video_end_date_time = datetime.fromtimestamp(Path(video_path).stat().st_mtime)
        pbar.update()
        text_height = h - TEXT_OFFSET
        while pbar.n <= total_frames:
            _, frame = video.read()  # Success is ignored since the videos that we are dealing with are stable.
            time_offset = timedelta(seconds=((total_frames - pbar.n) / fps))
            timestamp = (video_end_date_time - time_offset).strftime(DATE_TIME_FORMAT)
            putText(frame, timestamp, (TEXT_OFFSET, text_height), FONT_HERSHEY_SIMPLEX, 1, WHITE, 1)
            writer.write(frame)
            pbar.update()
    video.release()
    writer.release()
    print('Added Timestamps to Video!')


def _merge_audio_and_video(video_input_path: str, output_path: str) -> None:
    """
    For some reason, merging audio with video doesn't work with MoviePy currently, so ffmpeg-python is used instead to
    perform this process.

    :param video_input_path: the path to the video that supplied the video and audio in the processing pipeline.
    :param output_path: the path to the directory that will contain
    """
    print('Merging Audio and Timestamped Video...')
    audio, video = input(TEMP_AUDIO_FILE_NAME), input(TEMP_TIMESTAMPED_VIDEO_FILE_NAME)
    video_output_path = join(output_path, splitext(basename(video_input_path))[0] + '.mp4')
    concat(video, audio, v=1, a=1).output(video_output_path, preset='veryslow').run()
    remove(TEMP_AUDIO_FILE_NAME)
    remove(TEMP_TIMESTAMPED_VIDEO_FILE_NAME)
    print('Merged Audio and Timestamped Video!')


def timestamp_video(video_path: str, output_path: str) -> None:
    """
    Converts a MOD file to an MP4. If add_timestamps is True, then timestamps are added to the video in the bottom-left
    corner of the screen.

    :param video_path: the path to the MOD video that is to be converted to an MP4.
    :param output_path: the path to the output directory where the timestamped video should be saved.
    """
    print(f'Timestamping "{video_path}"...')
    _extract_audio(video_path)
    _timestamp_frames(video_path)
    _merge_audio_and_video(video_path, output_path)
    print(f'Timestamped "{video_path}"!')


def main():
    parser = ArgumentParser()
    parser.add_argument('-input_path', type=str, required=True, help='The directory that contains the input videos')
    parser.add_argument('-output_path', type=str, required=True, help="The directory that'll contain the output videos")
    args = parser.parse_args()
    input_path, output_path = args.input_path, args.output_path
    Path(output_path).mkdir(parents=True, exist_ok=True)

    for file_name in listdir(input_path):
        if f'{splitext(file_name)[0]}.mp4' in listdir(output_path):  # If the video has already been timestamped.
            print(f'"{file_name}" has already been timestamped.')
        elif file_name.upper().endswith('MOD') or file_name.lower().endswith('mp4'):  # If it is a MOD or an MP4 file.
            timestamp_video(join(input_path, file_name), output_path)


if __name__ == '__main__':
    main()
