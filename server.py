import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def get_video():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'लिंक नहीं मिला'}), 400

    ydl_opts = {'format': 'best', 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if video_url:
                return jsonify({'video_url': video_url})
            return jsonify({'error': 'वीडियो लिंक नहीं निकल पाया'}), 400
    except Exception:
        return jsonify({'error': 'वीडियो नहीं मिला (पब्लिक Reel ही डालें)'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)