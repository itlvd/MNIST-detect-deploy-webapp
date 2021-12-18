from keras.models import load_model
import gradio as gr
import numpy as np
model = load_model('./data/mnist_model.h5')

def predict_image(img):
  print(img)
  img_3d=img.reshape(-1,28,28)
  im_resize=img_3d/255.0
  prediction=model.predict(im_resize)
  pred=np.argmax(prediction)
  return pred

iface = gr.Interface(predict_image, inputs="sketchpad", outputs="label")
iface.launch(debug='True')