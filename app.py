import numpy as np
import pandas as pd
import json, base64, io
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import image
from flask import Flask, request, jsonify, render_template
# from keras.models import load_model
import cv2


UPLOAD_FOLDER = './uploads'
app = Flask(__name__,static_folder='static',template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# model = load_model('./model/digit_recog_model.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        content = request.get_json()
        img1 = content['img1']
        img1 = img1[img1.find(',')+1:]

        math_symbol = content['math_symbol']
        math_symbol = math_symbol[math_symbol.find(',')+1:]

        img2 = content['img2']
        img2 = img2[img2.find(',')+1:]

        save_img(img1, "img1.jpg")
        save_img(math_symbol, "math_symbol.jpg")
        save_img(img2, "img2.jpg")
        predict_numbers()

    return jsonify({"received": "yes"})

def save_img(img, filename):
    img = base64.b64decode(img)
    with open(filename, "wb") as f:
        f.write(img)
    # predict()

def predict_numbers():
    img1 = cv2.imread('img1.jpg', cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread('img2.jpg', cv2.IMREAD_GRAYSCALE)
    num_arr = [img1, img2]
    model = load_model('./model/digit_recog_model.h5')
    predictions = []
    for x in num_arr:
        img = cv2.resize(x, (28, 28), interpolation=cv2.INTER_AREA)
        img_data = np.asarray(img)
        img_data = np.round(img_data) / 255
        img_data = img_data[..., np.newaxis]
        pred = model.predict(np.expand_dims(img_data, axis=0))
        class_ = np.argmax(pred[0])
        predictions.append(class_)
    print(predictions)
    # return jsonify(predictions)

if __name__ == "__main__":
    app.run(debug=True)