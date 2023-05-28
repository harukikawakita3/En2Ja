from pydub import AudioSegment

# オーディオファイルを読み込む
audio_file = AudioSegment.from_file("opm/part0.mp3", format="mp3")

# 分割する秒数（5分=300秒）
split_sec = 20

# 分割したい間隔（ms単位）
split_interval = split_sec * 1000

# 分割したオーディオファイルを保存するディレクトリ
output_dir = "opm/"

# オーディオファイルを指定した時間ごとに分割する
for i, chunk in enumerate(audio_file[::split_interval]):
    # 分割したオーディオファイルを保存する
    chunk.export(output_dir + f"mini{i}.mp3", format="mp3")

print('successfully')