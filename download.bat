@echo off
chcp 65001
cd yt-dlp
yt-dlp -a ..\download-list.txt -x -o "..\downloads\%%(upload_date)s-%%(title)s.%%(ext)s" --audio-format mp3
pause