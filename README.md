# Behavioral Cloning

## 1. Goals and Steps

---

**Behavioral Cloning Project**

This project perfoms behavioral cloning, training an CNN model to mimic human driving behavior. The training data is collected by driving the car in the simulator. A deep nueral network is used to train the camera image data and predict the steering angle. The goals/steps of this project are the following:

* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report

## 2. Rubric Points

**Here I will consider the rubic points individually and describe how I addressed each point in my implementation.**

---
### 2.1 Files Submitted & Code Quality

#### 2.1.1 Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model (model architechture)
* drive.py for driving the car in autonomous mode
* model.json containing a trained convolution neural network (model weights) 
* writeup_report.md summarizing the results

#### 2.1.2 Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.json
```

#### 2.1.3 Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### 2.2 Model Training Strategy

---
#### 2.2.1 Data Augmentation

I drove 5 laps around the track:

* 2 laps of center lane driving
* 1 lap of recovery driving from the sides
* 1 lap of driving smoothly around curves
* 1 lap of clockwise driving(inverse direction)

I collected the front, left and right camera images from the simulator. Before training the neural network I used data augmentation as follows:

* Double the data set by horizontally flipping all training images and inverted the steering angle
* Add +/-0.15 angle offset to steering angle for the normal driving data
* Drop the front images and add an angle offset of +/-0.5 to the steering angle for the recovery data 
* Smooth data by moving average with a window  of 0.3 seconds

Using the left/right images is useful to train the recovery driving scenario. The horizontal flip is useful for difficult curve handling.

#### 2.2.2 Data Proprocessing

In order to gauge how well the model was working, I randomly shuttle the data and split my image and steering angle data into a training (90%) and validation (10%) set. I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The test is not used in this project as we do not need to test the generalization probability of the CNN models.

### 2.3 Model Architecture and Training Strategy

---

#### 2.3.1 An appropriate model architecture has been employed

The design of the network is based on comma.ai's model, whicho is a simple model. It is a deep convolutional nueral network which works well with supervised image calssification problems. I adjust the training images to produce the best result with some adjustments t the model to avoid overfitting. The final model is as follows:

* Image normalization: Lambda layer
* Convolution: 8x8, strides: 4, depth: 16, same padding, activation: ELU
* Convolution: 5x5, strides: 2, depth: 32, same padding, activation: ELU
* Convolution: 5x5, strides: 2, depth: 64, same padding
* Drop out (0.2)
* Activation: ELU
* Fully-connected: neurons: 512, activation: ELU
* Drop out (0.5)
* Activation: ELU
* Fully-connected: neurons: 1

My model consists of a convolution neural network with 5 traineable layers. The model follows the standard design practice for CNN: the base convolutional layer's height and width progressively decrese while its depth increases, and the final layers are a series fo fully-connected layers. Dropout layers were used to help reduce overfitting.


#### 2.3.2 Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting.

The model was trained and validated on different data sets to ensure that the model was not overfitting. The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 2.3.3 Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually.

#### 2.3.4 Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road. The details can be seen in data augmentation and preprocessing part.

The final step was to run the simulator to see how well the car was driving around track one. At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

---
