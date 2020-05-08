import numpy as np
import pandas as pd
import json, base64, io
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import image
from flask import Flask, request, jsonify, render_template
from keras.models import load_model
import cv2
from os import listdir
from os.path import isfile, join


UPLOAD_FOLDER = './uploads'
app = Flask(__name__,static_folder='static',template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

result = {}
# digit_model = load_model('./model/digit_recog_model.h5')
# operation_model = load_model('./model/operation_recog_model.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        global result
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
        predict_operation()

    return jsonify(result)

"""
# used for gathering operations data
@app.route('/gatherimgdata', methods=['GET', 'POST'])
def gatherimgdata():
    if request.method == 'POST':
        content = request.get_json()

        math_symbol = content['math_symbol']
        math_symbol = math_symbol[math_symbol.find(',')+1:]

        mypath = './divisionimgs'
        img_name = "division"
        start_read_filename = int(len("division_"))

        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        if len(onlyfiles) > 0:
            indices = [int(f[start_read_filename:-4]) for f in onlyfiles]
            ind = max(indices)
            newind = ind+1
        else:
            newind = 1

        save_img(math_symbol, f"./{mypath}/{img_name}_{newind}.jpg")
        # predict_numbers()

    return jsonify({"saved": "yes"})
"""

def save_img(img, filename):
    img = base64.b64decode(img)
    with open(filename, "wb") as f:
        f.write(img)

def predict_numbers():
    global result
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
        class_percentage = pred[0][class_]
        predictions.extend([str(class_), str(class_percentage)])
    result['num_1'] = str(predictions[0])
    result['num_1_perc'] = str(predictions[1])
    result['num_2'] = str(predictions[2])
    result['num_2_perc'] = str(predictions[3])


def predict_operation():
    global result
    img = cv2.imread('math_symbol.jpg', cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
    model = load_model('./model/operation_recog_model.h5')
    img_data = np.asarray(img)
    img_data = np.where(img_data > 0, 1, 0)
    img_data = img_data[..., np.newaxis]
    pred = model.predict(np.expand_dims(img_data, axis=0))
    class_ = np.argmax(pred[0])
    class_percentage = pred[0][class_]
    if class_ == 0:
        ans = "+"
    elif class_ == 1:
        ans = "-"
    elif class_ == 2:
        ans = "*"
    elif class_ == 3:
        ans = "/"
    else:
        ans = "unrecognized"
    result['op'] = str(ans)
    result['op_perc'] = str(class_percentage)


if __name__ == "__main__":
    app.run(debug=True)