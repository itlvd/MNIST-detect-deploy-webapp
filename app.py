import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from keras.models import load_model
import numpy as np

# Specify canvas parameters in application
stroke_width = st.sidebar.slider("Stroke width: ", 1, 5, 5)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image= None,
    update_streamlit=True,
    height=112,
    width=112,
    drawing_mode="freedraw",
    key="canvas",
)

# Do something interesting with the image data and paths
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)

def convert2D(img):
    image= []
    D1 = len(img)
    D2 = len(img[0])
    for i1 in range(D1):
        row = []
        for i2 in range(D2):
            number = int((img[i1][i2][0] + img[i1][i2][1]+img[i1][i2][2])/3)
            ret = int((number + (-2*127.5))*-1)
            if(ret > 127):
                ret = 255
            else:
                ret = 0
            row.append(ret)
        image.append(row)
    return np.array(image)

def label(pred):
    return np.argmax(pred)


model = load_model('./data/mnist_model.h5')
if canvas_result.image_data is not None:
    imt = canvas_result.image_data[:,:,:3] #delete alpha channel
    #convert hex color to rbg color
    img = convert2D(imt)

    img_pil = Image.fromarray(img)
    img_28x28 = np.array(img_pil.resize((28, 28), Image.ANTIALIAS))

    img_3d=img_28x28.reshape(-1,28,28)
    im_resize=img_3d/255.0
    y_pred = model.predict(im_resize)
    st.text("Predict: ")
    st.write(label(y_pred))
    st.write(y_pred)