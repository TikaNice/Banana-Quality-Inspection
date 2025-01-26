from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

#Function for use training model 
def banana_model_predict(image_path):
    #Loading model
    model = load_model('/Users/jimpengdemg/Documents/我的项目/Qhack/2025/fruit-identification/src/model_and_use/banana_status_classifier.h5')
    #Output type/label
    classes = ['Unripe', 'Ripe', 'Rot']
    
    img = load_img(image_path, target_size=(224, 224))  
    img_array = img_to_array(img) / 255.0  
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    class_idx = prediction.argmax()
    return classes[class_idx]