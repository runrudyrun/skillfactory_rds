import streamlit as st
import pandas as pd
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from utils import *
from model.model import *
from PIL import Image

predictor = Predictor(mode = 'float')
images = []
preds = []
chip_maker = ChipCreator(64)

st.write('Here you can upload your own pictures of any shape (1024x1024 is preferred for this prototype)')
uploaded_files = st.file_uploader("Choose 2 pictures", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    if uploaded_file != None:
        image = Image.open(uploaded_file)
        images.append(image)
        st.image(image, caption='Uploaded Image.', use_column_width=True)

if st.button('make_prediction'):
    st.title('Prediction:')
    if len(images) == 2:
        im1 = chip_maker.make_chips(np.array(images[0]))
        im2 = chip_maker.make_chips(np.array(images[1]))
        for i in range(len(im1)):
            preds.append(Predictor(encode(im1[i][:,:,:3],im2[i][:,:,:3])))
        preds = np.array(preds)
        preds = preds.reshape(16,16,64,64).swapaxes(1,2).reshape(1024,1024) 
        st.pyplot(plt.imshow(preds))
    else:
        st.write("Download two pictures first")