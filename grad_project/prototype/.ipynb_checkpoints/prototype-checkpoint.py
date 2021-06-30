import streamlit as st
import pandas as pd
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from utils import *
from model.model import *
from PIL import Image



DATA_DIR = '../SpaceNet/chip_dataset/change_detection/'
ANN = './annotations/df.csv'
annotations = pd.read_csv(ANN)
predictor = Predictor(mode = 'float')
predictions = []
y_hat = np.zeros((64,64))

st.title('Satellite change detection prototype')
st.write('Here you can draw random chip pair to test algorithm')
if st.button('random_pick'):
    im1,im2,mask = get_random_chip_pair(annotations, DATA_DIR)
    for i in range(100):
        # test_time augmentation
        y_hat += predictor(encode(im1,im2))
    y_hat = y_hat/100
    fig, axes = plt.subplots(1,4)
    axes[0].imshow(im1)
    axes[0].set_title('image_1')
    axes[1].imshow(im2)
    axes[1].set_title('image_2')
    axes[2].imshow(mask)
    axes[2].set_title('ground_truth')
    axes[3].imshow(y_hat)
    axes[3].set_title('predict')
    fig.tight_layout()
    st.pyplot(fig)
    st.write(f'IoU:{iou(mask,y_hat):2f}')




