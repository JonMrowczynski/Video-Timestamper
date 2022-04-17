@echo off
title correlator build script
del /Q build, dist
python -O -m PyInstaller --clean --onefile video_timestamper.py