from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import ffmpeg

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(output_path='downloads/', filename='video.mp4')

    # Convert to desired format using ffmpeg
    input_file = 'downloads/video.mp4'
    output_file = 'downloads/video_converted.mp4'
    ffmpeg.input(input_file).output(output_file).run()

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
