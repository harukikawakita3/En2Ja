from pathlib import Path
from flask import Flask, render_template, request
from app import remove_specific_timestamps, convert_vtt_to_srt, clean_title
from yt_dlp import YoutubeDL
import os
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from io import BytesIO
import numpy as np

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


### image_recognition

mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images / 255.0
test_images = test_images / 255.0  # Normalize the test images

# Cache the model to avoid retraining it every time
model = None
def get_model():
    global model
    if not model:
        # Construct the model
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(10, activation='softmax')
        ])

        # Compile the model
        model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])

        # Train the model
        model.fit(train_images, train_labels, epochs=10)

        # Evaluate the model with test data
        test_loss, test_acc = model.evaluate(test_images, test_labels)
        print('Test accuracy:', test_acc)

    return model

@app.route('/image_recognition', methods=['GET', 'POST'])
def image_recognition():
    if request.method == 'POST':
        # Check if the file is uploaded
        if 'image' not in request.files:
            return render_template('image_recognition.jinja', error='No file selected.')

        # Read the image file and preprocess it
        image_file = request.files['image']
        image = Image.open(BytesIO(image_file.read())).convert('L')
        image = image.resize((28, 28))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        # Load the model and predict the digit in the image
        model = get_model()
        prediction = model.predict(image)
        predicted_digit = np.argmax(prediction)

        return render_template('image_recognition.jinja', image=image, predicted_digit=predicted_digit)

    return render_template('image_recognition.jinja')

if __name__ == '__main__':
    app.run(debug=True)
#host="0.0.0.0"

