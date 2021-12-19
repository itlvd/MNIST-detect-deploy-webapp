import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from keras.models import load_model
import numpy as np

# Specify canvas parameters in application
stroke_width = 5
stroke_color = "black"
bg_color = "#eee"

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

def scale112pxTo28Px(img):
    D1 = len(img)
    D2 = len(img[0])
    ret = []
    img = np.array(img)
    for row in range(0,D1,4):
        matrixRow = []
        for col in range(0,D2,4):
            subMatrix = img[row:row+4,col:col+4]
            meanOfMatrix =int(np.mean(subMatrix))
            if meanOfMatrix > 127:
                meanOfMatrix = 255
            else:
                meanOfMatrix = 0
            matrixRow.append(meanOfMatrix)
        ret.append(matrixRow)
    return np.array(ret)


model = load_model('./data/mnist_model.h5')
if canvas_result.image_data is not None:
    imt = canvas_result.image_data[:,:,:3] #delete alpha channel
    #convert hex color to rbg color
    img = convert2D(imt)

    img_28x28 = scale112pxTo28Px(img)

    img_3d=img_28x28.reshape(-1,28,28)
    im_resize=img_3d/255.0
    y_pred = model.predict(im_resize)
    st.text("Predict: ")
    st.write(label(y_pred))
    st.write(y_pred)