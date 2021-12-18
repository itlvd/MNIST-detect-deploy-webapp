import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from keras.models import load_model

# Specify canvas parameters in application
stroke_width = st.sidebar.slider("Stroke width: ", 1, 28, 28)
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
    height=28,
    width=28,
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

model = load_model('./data/mnist_model.h5')
image = canvas_result.image_data[:,:,:3]
st.write(image)
if canvas_result.image_data is not None:
    image = canvas_result.image_data[:,:,:0]
    st.write(image.shape)
    y_pred = model.predict(image)
    st.text("Predict: ")
    st.write(y_pred)