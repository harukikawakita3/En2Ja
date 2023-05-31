import re
from webvtt import WebVTT

def clean_title(title):
    title = re.sub('-[A-Za-z0-9]+\.en', '', title)  # Remove video ID and language code
    title = re.sub('[\W_]+', '_', title)  # Replace non-alphanumeric characters with underscore
    title = re.sub('\s+', '_', title)  # Replace spaces with underscore
    title = title[:32]  # Limit the length of the title to avoid too long filename
    return title

def convert_vtt_to_srt(subtitle_path):
    srt_captions = ""
    captions = WebVTT().read(subtitle_path)
    for index, caption in enumerate(captions):
        start_time = caption.start_in_seconds
        end_time = caption.end_in_seconds
        text = caption.text.replace("\n", "\\n")
        srt_captions += f"{index + 1}\n{start_time} --> {end_time}\n{text}\n\n"
    return srt_captions

def remove_specific_timestamps(text):
    pattern = re.compile(r'^\d+\n\d+\.?\d* --> \d+\.?\d*\n', re.MULTILINE)
    text_without_specific_lines = pattern.sub('', text)
    return text_without_specific_lines
