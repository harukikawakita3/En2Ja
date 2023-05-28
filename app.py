# import openai
# import os

# openai.api_key = os.environ["OPENAI_API_KEY"]

# audio_file = open("opm/part0.mp3", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)['text']
# filename = 'opt/devate.txt'

# with open(filename, "w", encoding='utf-8') as file:
#     file.write(transcript)

# print('successfully')


import openai
import os
import re
from webvtt import WebVTT

# def initialize_openai(api_key):
#     openai.api_key = api_key

def transcribe(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def write_transcript_to_file(transcript, filename):
    with open(filename, "w", encoding='utf-8') as file:
        file.write(str(transcript))
    print('Successfully written transcript to file.')

def clean_title(title):
    title = re.sub('-[A-Za-z0-9]+\.en', '', title)  # Remove video ID and language code
    title = re.sub('[\W_]+', '_', title)  # Replace non-alphanumeric characters with underscore
    title = re.sub('\s+', '_', title)  # Replace spaces with underscore
    title = title[:100]  # Limit the length of the title to avoid too long filename
    return title

def convert_vtt_to_srt(subtitle_path):
    captions = WebVTT().read(subtitle_path)
    srt_captions = ""
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
