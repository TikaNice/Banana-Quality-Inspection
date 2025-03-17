from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from model_and_use import banana_model
# 创建Flask应用程序实例

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = './upload_images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

#Check the input file is image or not 
def allowed_image(file_name):
    return "." in file_name and file_name.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/api/Banana_ripeness_status_identification", methods=['POST','OPTIONS'])
def Banana_ripeness_status_identification():
    if request.method == 'OPTIONS':
        response = app.response_class(status=204)
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    if 'file' not in request.files:
        return jsonify({'error': "Can't find file"}),400
    
    file = request.files["file"]
    print("Received file:", file)
    
    if file.filename == '':
        return jsonify({'error': "filename is empty"}),400
    
    if file and allowed_image(file.filename):
        file_name =secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(filepath)
    
    try:
        banana_status = banana_model.banana_model_predict(filepath)
        return jsonify({"Status":banana_status})
    except:
        return jsonify({'error': "Can't analysis file"})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
    
    
    
    