from pathlib import Path
from flask import Flask, render_template, request
from app import remove_specific_timestamps, convert_vtt_to_srt, clean_title
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    subtitle_path = None
    subtitle_filename = None

    if request.method == 'POST':
        url = request.form['url']

        with YoutubeDL() as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                subtitle_filename = clean_title(info['title'])
            except Exception:
                return render_template('index.jinja', error=f"{subtitle_filename} {subtitle_path} Invalid URL or unable to extract video information.")

        ydl_options = {
            'writesubtitles': True,
            'skip_download': True,
            'outtmpl': subtitle_filename,
            'writeautomaticsub': True
        }

        with YoutubeDL(ydl_options) as ydl:
            try:
                ydl.download([url])
                subtitle_path = Path(str(subtitle_filename) + '.en.vtt')
            except Exception:
                return render_template('index.jinja', error=f"{subtitle_filename} {subtitle_path} Unable to download video information.")

        if not subtitle_path.is_file():
            return render_template('index.jinja', error=f"Subtitle file does not exist. {subtitle_filename} {str(subtitle_path)}")

        subtitle_srt = convert_vtt_to_srt(subtitle_path)

        subtitles_remove_timestamps = remove_specific_timestamps(subtitle_srt)

        if not subtitles_remove_timestamps:
            return render_template('index.jinja', error="Subtitle file is empty")

        with open(f'dlm/{subtitle_filename}.txt', 'w') as f:
            f.write(subtitles_remove_timestamps)

        with open(f'dlm/{subtitle_filename}.srt', 'w') as f:
            f.write(subtitle_srt)

        if subtitle_path.is_file():
            # .vttファイルが存在する場合、削除します
            os.remove(subtitle_path)

        return render_template('index.jinja', subtitles=subtitles_remove_timestamps, vtt=subtitle_path, srt=subtitle_srt)

    return render_template('index.jinja')

if __name__ == '__main__':
    app.run()
#host="0.0.0.0"
