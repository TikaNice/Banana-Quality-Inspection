from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import requests
from io import BytesIO
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array

# Create flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set parameters
MODEL_URL = "https://github.com/TikaNice/fruit-classification-model/releases/download/v1.0/banana_status_classifier.h5"
CLASS_NAMES = ['Unripe', 'Ripe', 'Rot']  
TARGET_SIZE = (224, 224)  

# 全局缓存模型（避免重复下载）
_model = None

def load_remote_model():
    global _model
    if _model is None:
        try:
            print("Downloading model from GitHub...")
            response = requests.get(MODEL_URL)
            response.raise_for_status()
            
            # 从内存加载模型
            _model = load_model(BytesIO(response.content))
            print("Model loaded successfully")
        except Exception as e:
            print(f"Model load failed: {str(e)}")
            raise
    return _model

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

@app.route("/api/Banana_ripeness_status_identification", methods=['POST', 'OPTIONS'])
def predict():
    # 处理OPTIONS预检请求
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request accepted"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    # 加载模型
    try:
        model = load_remote_model()
    except:
        return jsonify({"error": "Model initialization failed"}), 500

    # 处理文件上传
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    try:
        # Temporary save file to disk
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            file.save(tmp.name)
            
            # preprocess image
            img = load_img(tmp.name, target_size=TARGET_SIZE)
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Using the model, doing prediction
            prediction = model.predict(img_array)
            class_idx = np.argmax(prediction)
            banana_status = CLASS_NAMES[class_idx]
            
            return jsonify({
                "Status": banana_status,
                "Confidence": float(np.max(prediction))
            })
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({"error": "Can't analyze file"}), 500

if __name__ == '__main__':
    app.run(debug=True)
