from flask import Flask, request
import os
from werkzeug.utils import secure_filename
# from ocr import ocr
from baidu_ocr import baidu_ocr

app = Flask(__name__)

# 设置上传文件夹
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    print(file_path)
    baidu_ocr(file_path)

    return f'File uploaded successfully: {filename}', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)