# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import argparse
import base64
import json

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import time
from PIL import Image
from PIL import ImageOps
from flask import Flask, render_template
from io import BytesIO

from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array
import tensorflow as tf
#tf.python.control_flow_ops = tf  
#%%
sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

# Inupt image dimensions
H, W, CH = 160, 320, 3

#%%
@sio.on('telemetry')
def telemetry(sid, data):
	steering_angle = data["steering_angle"]
	throttle = data["throttle"]
	speed = data["speed"]
	imgString = data["image"]
	image = Image.open(BytesIO(base64.b64decode(imgString)))
	image = image.convert('RGB')
	image = image.resize((W, H), Image.ANTIALIAS)
	image = np.asarray(image, dtype='float32')
	image = image[None, :, :, :]
	transformed_image_array = image
	steering_angle = float(model.predict(transformed_image_array, batch_size=1))
	
	if abs(steering_angle) < 0.03:
		throttle = 0.25
	elif abs(steering_angle) < 0.4:
		throttle = 0.15
	else:
		throttle = -0.5

	print('steering angle: %.4f, throttle: %.4f' % (steering_angle, throttle))
	send_control(steering_angle, throttle)


@sio.on('connect')
def connect(sid, environ):
	print("connect ", sid)
	send_control(0, 0)


def send_control(steering_angle, throttle):
	sio.emit("steer", data={
	'steering_angle': steering_angle.__str__(),
	'throttle': throttle.__str__()
	}, skip_sid=True)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Remote Driving')
	parser.add_argument('model', type=str,
	help='Path to model definition json. Model weights should be on the same path.')
	args = parser.parse_args()
	with open(args.model, 'r') as jfile:
		model = model_from_json(jfile.readline())

	model.compile("adam", "mse")
	weights_file = args.model.replace('json', 'h5')
	model.load_weights(weights_file)
	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('', 4567)), app)