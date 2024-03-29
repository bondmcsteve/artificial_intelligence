# -*- coding: utf-8 -*-
"""Copy of Andy - G1.1 MNIST with LeNet

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QKMRfo7nRp1re3SDgDVdI71PcPfujngq

# MNIST with MLP and LeNet
Understanding and Implementing LeNet-5 CNN Architecture

Reference:
1.   [Richmond Alake](https://towardsdatascience.com/understanding-and-implementing-lenet-5-cnn-architecture-deep-learning-a2d531ebc342)
2.   [Jeff Heaton](https://colab.research.google.com/github/jeffheaton/t81_558_deep_learning/blob/master/t81_558_class_06_2_cnn.ipynb)

# 1. Dataset Preparation
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load the dataset
num_classes = 10
input_shape = (28, 28, 1)

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
#(x_train, y_train), (x_test, y_test) = keras.datasets.fashion_mnist.load_data()

# Commented out IPython magic to ensure Python compatibility.
# OPTIONAL: Display some dataset samples as an image 
# %matplotlib inline
import matplotlib.pyplot as plt
import random

ROWS = 6
random_indices = random.sample(range(x_train.shape[0]), ROWS*ROWS)
sample_images = x_train[random_indices, :]
plt.clf()

fig, axes = plt.subplots(ROWS,ROWS, 
                         figsize=(ROWS,ROWS),
                         sharex=True, sharey=True) 

for i in range(ROWS*ROWS):
    subplot_row = i//ROWS 
    subplot_col = i%ROWS
    ax = axes[subplot_row, subplot_col]

    plottable_image = np.reshape(sample_images[i,:], (28,28))
    ax.imshow(plottable_image, cmap='gray_r')
    
    ax.set_xbound([0,28])

plt.tight_layout()
plt.show()

# Normalize images to the [0, 1] range
# This is to make the calculations more efficient
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# convert class label vectors to binary class matrices (convert to 1-hot format)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Commented out IPython magic to ensure Python compatibility.
# OPTIONAL: Use tensorboard to display graphs
# Load the TensorBoard notebook extension
# %load_ext tensorboard

import datetime
# create keras TensorBoard callback
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# specify the log directory
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

"""# 2. Select/Design Model

Choose one of these models to train. DO NOT RUN ALL CELLS HERE. Just choose one, then see the output.
"""

# 2-layer NN
model = keras.Sequential(
    [
      layers.Flatten(input_shape=(28, 28)),   # Input layer
      layers.Dense(100, activation='relu'),    # Hidden layer(s)
      layers.Dense(num_classes, activation='softmax')  # Output layer
    ]
)
model.summary()

# CNN LeNet model
model = keras.Sequential(
    [
      keras.Input(shape=input_shape),
      layers.Conv2D(32, kernel_size=(3, 3), activation='relu'), #C1
      layers.MaxPooling2D(pool_size=(2, 2)), #S2
      layers.Conv2D(32, kernel_size=(3, 3), activation='relu'), #C3
      layers.MaxPooling2D(pool_size=(2, 2)), #S4
      layers.Flatten(), #Flatten
      layers.Dense(64, activation='relu'), #C5
      layers.Dense(num_classes, activation='softmax') #Output layer
    ]
)
model.summary()

# LeNet-5 model
model = keras.Sequential(
    [
      layers.Conv2D(10, kernel_size=5, strides=1,  activation='relu', padding='same', input_shape=x_train[0].shape), #C1
      layers.AveragePooling2D(), #S2
      layers.Conv2D(16, kernel_size=5, strides=1, activation='relu', padding='valid'), #C3
      layers.AveragePooling2D(), #S4
      layers.Flatten(), #Flatten
      layers.Dense(120, activation='relu'), #C5
      layers.Dense(84, activation='relu'), #F6
      layers.Dense(num_classes, activation='softmax') #Output layer
    ]
)
model.summary()

"""# 3. Train the model"""

# set the loss, optimizer and metrics
model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adam(learning_rate=0.01), metrics=["accuracy"])

# train/fit the model
model.fit(x_train, y_train, batch_size=128, epochs=5, validation_split=0.1)

# Evaluate the trained model performance
score = model.evaluate(x_test, y_test)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Use Tensorboard to show graphs
# train the model and save training performance parameters into training_history
training_history = model.fit(
    x_train, # input data 
    y_train, # output classes
    batch_size=128, 
    epochs=20, 
    validation_split=0.1, 
    verbose=0, # Suppress chatty output; use Tensorboard instead 
    validation_data=(x_test, y_test),
    callbacks=[tensorboard_callback],
)

tensorboard --logdir logs/fit

"""# 4. Test the trained model

### 4a. For Numbers/Digit MNIST, make a canvas for user to draw a digit
"""

# Make a canvas for user to draw a digit
# then save the drawing as a png file
# source: https://gist.github.com/korakot/8409b3feec20f159d8a50b0a811d3bca
from IPython.display import HTML, Image
from google.colab.output import eval_js
from base64 import b64decode

canvas_html = """
<canvas width=%d height=%d></canvas>
<button>Finish</button>
<script>
var canvas = document.querySelector('canvas')
var ctx = canvas.getContext('2d')
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.lineWidth = %d
var button = document.querySelector('button')
var mouse = {x: 0, y: 0}

canvas.addEventListener('mousemove', function(e) {
  mouse.x = e.pageX - this.offsetLeft
  mouse.y = e.pageY - this.offsetTop
})
canvas.onmousedown = ()=>{
  ctx.beginPath()
  ctx.moveTo(mouse.x, mouse.y)
  canvas.addEventListener('mousemove', onPaint)
}
canvas.onmouseup = ()=>{
  canvas.removeEventListener('mousemove', onPaint)
}
var onPaint = ()=>{
  ctx.lineTo(mouse.x, mouse.y)
  ctx.stroke()
}

var data = new Promise(resolve=>{
  button.onclick = ()=>{
    resolve(canvas.toDataURL('image/png'))
  }
})
</script>
"""

def draw(filename='drawing.png', w=150, h=150, line_width=10):
  display(HTML(canvas_html % (w, h, line_width)))
  data = eval_js("data")
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
    print("image saved as: ")
    print(filename)
  # return len(binary)

draw()

import matplotlib.pyplot as plt
from PIL import Image, ImageOps # import pillow image manipulation tool

# Load the image to be tested
user_image = Image.open('drawing.png')
user_image = ImageOps.grayscale(user_image)

# Resize to input_shape
user_image = user_image.resize((input_shape[0],input_shape[1]))
plt.imshow(user_image, cmap='gray', vmin=0, vmax=255)

# invert color if background is white. if background is black, comment out the following line.
user_image = ImageOps.invert(user_image)  

user_image = np.array(user_image).astype("float32") / 255
# user_image = np.expand_dims(user_image, axis=0)
user_image = user_image.reshape(-1, 28, 28, 1)
# print("user_image shape:", user_image.shape)

# Predict the class of the drawing 
result = model.predict(user_image)
print(result)
result = np.argmax(result,axis=1)
print("The AI thinks this is class:", result[0])

"""### 4b. For Fashion MNIST, upload a sample picture"""

LABEL_NAMES = ['t_shirt', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt', 'sneaker', 'bag', 'ankle_boots']

from google.colab import files
uploaded = files.upload()

filename = next(iter(uploaded))

import matplotlib.pyplot as plt
from PIL import Image, ImageOps # import pillow image manipulation tool

# Load the image to be tested
user_image = Image.open(filename)
user_image = ImageOps.grayscale(user_image)

# Resize to input_shape
user_image = user_image.resize((input_shape[0],input_shape[1]))
plt.imshow(user_image, cmap='gray', vmin=0, vmax=255)

# invert color if background is white. if background is black, comment out the following line.
user_image = ImageOps.invert(user_image)

user_image = np.array(user_image).astype("float32") / 255
# user_image = np.expand_dims(user_image, axis=0)
user_image = user_image.reshape(-1, 28, 28, 1)
# print("user_image shape:", user_image.shape)

# Predict the class of the drawing 
result = model.predict(user_image)
print(result)
result = np.argmax(result,axis=1)
print("The output class is:", result[0])
print("The AI thinks this is the garment:", LABEL_NAMES[result[0]])