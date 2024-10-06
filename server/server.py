from flask import Flask, jsonify, request, render_template
import tensorflow as tf
from tensorflow import keras
from keras import models
import os
import pickle
import numpy as np
# import serial

# arduino = serial.Serial('COM4', 9600)

app = Flask(__name__)

__answer = None
__model = None
__classes = [
    'Aluminium',
    'Carton',
    'Glass',
    'Organic Waste',
    'Other Plastics',
    'Paper and Cardboard',
    'Plastic',
    'Textiles',
    'Wood'
]

def loadModel(model_path):
    global __model
    if os.path.exists(model_path):
        __model = models.load_model(model_path,compile=False)
        print("Model loaded successfully.")
    else:
        print(f"Error: File not found at path '{model_path}'")

@app.route('/test', methods=['GET'])
def test():
    return "Hi"

def getLatest():
    directory_path = '/Users/rishabpendam/Downloads/IPD/server/images'
    all_files = os.listdir(directory_path)
    file_paths = [os.path.join(directory_path, file) for file in all_files if os.path.isfile(os.path.join(directory_path, file))]
    sorted_files = sorted(file_paths, key=lambda x: os.path.basename(x), reverse=True)
    latest_file_path = sorted_files[0] if sorted_files else None
    return latest_file_path

# Thread function to monitor COM4 port
# def com4_monitor():
#     while True:
#         if arduino.in_waiting > 0:
#             data = arduino.readline().decode().strip()
#             if data == "Dispose Waste":
#                 classifyWaste()

# @app.route('/classifyWaste', methods=['POST'])
def classifyWaste():
    global __model
    global __classes
    global __answer

    # if 'image' not in request.files:
    #     return "No file uploaded"

    # image_file = request.files['image']

    temp_image_path = getLatest()
    # image_file.save(temp_image_path)
    print(temp_image_path)

    image = tf.keras.utils.load_img(temp_image_path, target_size=(180, 180))
    image_arr = tf.keras.utils.img_to_array(image)
    image_fin = tf.expand_dims(image_arr, 0)
    # print(image_fin)

    result = np.argmax(__model.predict(image_fin))
    __answer = __classes[result]

    # os.remove(temp_image_path)
    print(__answer)

@app.route('/classify', methods=['GET'])
def classify():
    global __answer
    # answer = classifyWaste()
    answer = __answer
    return answer


if __name__ == '__main__':
    print("Server running....")
    model_path = os.path.abspath('/Users/rishabpendam/Downloads/IPD/server/artifacts/model_waste.h5')
    loadModel(model_path)
    classifyWaste()
    app.run(port=8000)
    # while True:
    #     choice = int(input("Enter\n1.To Dispose waste\n0.End code:\n"))
    #     if choice:
    #         classifyWaste()
    #     else:
    #         break
