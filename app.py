from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400

        video_url = data['url']
        download_dir = '/tmp/downloads'

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Çerezleri dahil et
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
            'cookies': 'cookies.txt'  # Çerez dosyasını belirtin
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(video_url, download=True)
                file_path = ydl.prepare_filename(info_dict)
            except Exception as e:
                print(f"Download error: {e}")
                return jsonify({'error': f'Failed to download video: {e}'}), 500

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to download video: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Server is running on port {port}")
    app.run(host='0.0.0.0', port=port)
