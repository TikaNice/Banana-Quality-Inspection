from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
from model_and_use import banana_model

def vercel_handler(request):
    return handle(app)(request)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 禁用本地文件存储（Vercel无法持久化存储）
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()  # 使用临时目录
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_image(file_name):
    return "." in file_name and file_name.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/api/Banana_ripeness_status_identification", methods=['POST','OPTIONS'])
def Banana_ripeness_status_identification():
    if request.method == 'OPTIONS':
        response = app.response_class(status=204)
        response.headers.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        })
        return response

    if 'file' not in request.files:
        return jsonify({'error': "Can't find file"}), 400
    
    file = request.files["file"]
    
    if file.filename == '':
        return jsonify({'error': "filename is empty"}), 400
    
    if not (file and allowed_image(file.filename)):
        return jsonify({'error': "File type not allowed"}), 400

    try:
        # 使用临时文件处理（自动清理）
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            file.save(temp_file.name)
            banana_status = banana_model.banana_model_predict(temp_file.name)
        
        return jsonify({"Status": banana_status})
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return jsonify({'error': "Can't analyze file"}), 500

# Vercel需要导出一个handler
handler = handle(app)
