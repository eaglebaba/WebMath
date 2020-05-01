import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import image
from keras.models import load_model
from PIL import Image
import cv2
import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
tf.get_logger().setLevel('INFO')

"""
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
"""



model = load_model('./model/digit_recog_model.h5')
images = ['img1.jpg', 'img2.jpg']
for the_image in images:
    img1 = cv2.imread(the_image, cv2.IMREAD_GRAYSCALE)
    plt.imshow(img1, cmap='Greys_r')
    plt.show()

    img1 = cv2.resize(img1, (28, 28), interpolation=cv2.INTER_AREA)
    plt.imshow(img1, cmap='Greys_r')
    plt.show()

    img1_data = np.asarray(img1)
    img1_data = np.round(img1_data) / 255

    img1_data = img1_data[..., np.newaxis]
    pred = model.predict(np.expand_dims(img1_data, axis=0))
    class_ = np.argmax(pred[0])
    print(class_)
    print(pred)