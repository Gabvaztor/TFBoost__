"""
Author: @gabvaztor
StartDate: 04/03/2017

This file contains samples and overrides deep learning algorithms.

Style: "Google Python Style Guide" 
https://google.github.io/styleguide/pyguide.html

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pandas.core.indexing import _iAtIndexer

"""
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# IMPORTS
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
"""

'''LOCAL IMPORTS'''
from UsefulTools.UtilsFunctions import *
from TFBoost.TFEncoder import Dictionary as dict
from TFBoost.TFEncoder import Constant as const
''' TensorFlow: https://www.tensorflow.org/
To upgrade TensorFlow to last version:
*CPU: pip3 install --upgrade tensorflow
*GPU: pip3 install --upgrade tensorflow-gpu
'''
import tensorflow as tf
print("TensorFlow: " + tf.__version__)


''' Numpy is an extension to the Python programming language, adding support for large,
multi-dimensional arrays and matrices, along with a large library of high-level
mathematical functions to operate on these arrays.
It is mandatory to install 'Numpy+MKL' before scipy.
Install 'Numpy+MKL' from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
http://www.numpy.org/
https://en.wikipedia.org/wiki/NumPy '''
import numpy as np

'''
# You need to install the 64bit version of Scipy, at least on Windows.
# It is mandatory to install 'Numpy+MKL' before scipy.
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
# We can find scipi in the url: http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy'''
import scipy.io as sio

''' Matlab URL: http://matplotlib.org/users/installing.html'''
import matplotlib.pyplot as plt
from pylab import *
''' TFLearn library. License MIT.
Git Clone : https://github.com/tflearn/tflearn.git
To install: pip install tflearn'''
import tflearn
'''"Best image library"
pip install opencv-python'''
import cv2

""" Random to suffle lists """
import random
""" Time """
import time

class TFModels():
    """
    Long Docs ...
    """
    # TODO Docs
    def __init__(self,input, test, input_labels, test_labels, number_of_classes, number_of_inputs=None,
                      learning_rate=1e-3, trains=None, type=None, validation=None,
                      validation_labels=None, deviation=None):
        self._input = input
        self._test = test
        self._input_labels = input_labels
        self._test_labels = test_labels
        self._number_of_inputs = number_of_inputs
        self._number_of_classes = number_of_classes
        self._learning_rate = learning_rate  # Learning rate
        self._inputs_processed = []  # New inputs processed for training. (Change during shuffle)
        self._labels_processed = []  # New labels processed for training. (Change during shuffle)
        # VARIABLES
        self._show_info = 0  # Labels and logits info.
        self._show_images = 0  # if True show images when show_info is True
        self._shuffle_data = True
        self._to_array = True  # If the images must be reshaped into an array
        self._input_rows_numbers = 60
        self._input_columns_numbers = 60
        self._kernel_size = [5, 5]  # Kernel patch size
        self._epoch_numbers = 100  # Epochs number
        self._batch_size = 100  # Batch size
        self._input_size = len(input)
        self._test_size = len(test)
        self._train_dropout = 0.5  # Keep probably to dropout to avoid overfitting
        self._index_buffer_data = 0  # The index for batches during training
        self._first_label_neurons = 50
        self._second_label_neurons = 55
        self._third_label_neurons = 50
        self._num_trains_count = 0
        if not trains:
            self._trains = int(self.input_size / self.batch_size) + 1
        else:
            self._trains = trains

    @property
    def show_info(self): return self._show_info

    @property
    def learning_rate(self): return self._learning_rate

    @property
    def show_images(self): return self._show_images

    @property
    def shuffle_data(self): return self._shuffle_data

    @property
    def to_array(self): return self._to_array

    @property
    def input_rows_numbers(self): return self._input_rows_numbers

    @property
    def input_columns_numbers(self): return self._input_columns_numbers

    @property
    def input_columns_after_reshape(self): return self.input_rows_numbers * self.input_columns_numbers

    @property
    def input_rows_columns_array(self): return [self.input_rows_numbers, self.input_columns_numbers]

    @property
    def kernel_size(self): return self._kernel_size

    @property
    def input_size(self): return self._input_size

    @property
    def test_size(self): return self._test_size

    @property
    def batch_size(self): return self._batch_size

    @property
    def train_dropout(self): return self._train_dropout

    @property
    def index_buffer_data(self): return self._index_buffer_data

    @index_buffer_data.setter
    def index_buffer_data(self, value): self._index_buffer_data = value

    @property
    def labels_processed(self): return self._labels_processed

    @labels_processed.setter
    def labels_processed(self, value): self._labels_processed = value

    @property
    def inputs_processed(self): return self._inputs_processed

    @inputs_processed.setter
    def inputs_processed(self, value): self._inputs_processed = value

    @property
    def first_label_neurons(self): return self._first_label_neurons

    @property
    def second_label_neurons(self): return self._second_label_neurons

    @property
    def third_label_neurons(self): return self._third_label_neurons

    @property
    def trains(self): return self._trains

    @trains.setter
    def trains(self, value): self._trains = value

    @property
    def num_trains_count(self): return self._num_trains_count

    @num_trains_count.setter
    def num_trains_count(self, value): self._num_trains_count = value

    @property
    def number_of_classes(self): return self._number_of_classes

    @property
    def input_labels(self): return self._input_labels

    @input_labels.setter
    def input_labels(self, value): self._input_labels = value

    @property
    def test_labels(self): return self._test_labels

    @property
    def epoch_numbers(self): return self._epoch_numbers

    @property
    def input(self): return self._input

    @input.setter
    def input(self, value): self._input = value

    @property
    def test(self): return self._test

    def actual_configuration(self):
        """
        Return a string with actual features
        """
        return self.__dict__

    @timed
    def convolution_model_image(self):
        """
        Generic convolutional model
        """

        pt('first_label_neurons', self.first_label_neurons)
        pt('second_label_neurons', self.second_label_neurons)
        pt('third_label_neurons', self.third_label_neurons)
        pt('input_size', self.input_size)
        pt('batch_size', self.batch_size)
        # TODO Try python EVAL method to do multiple variable neurons

        # Placeholders
        x = tf.placeholder(tf.float32, shape=[None, self.input_columns_after_reshape])  # All images will be 24*24 = 574
        y_ = tf.placeholder(tf.float32, shape=[None, self.number_of_classes])  # Number of labels
        keep_probably = tf.placeholder(tf.float32)  # Value of dropout. With this you can set a value for each data set

        x_reshape = tf.reshape(x, [-1, self.input_rows_numbers, self.input_columns_numbers,1])
        # Reshape x placeholder into a specific tensor

        # First Convolutional Layer
        convolution_1 = tf.layers.conv2d(
            inputs=x_reshape,
            filters=self.third_label_neurons,
            kernel_size=self.kernel_size,
            padding="same",
            activation=tf.nn.relu)
        # Pool Layer 1 and reshape images by 2
        pool1 = tf.layers.max_pooling2d(inputs=convolution_1, pool_size=[2, 2], strides=2)
        # Second Convolutional Layer

        convolution_2 = tf.layers.conv2d(
            inputs=pool1,
            filters=self.third_label_neurons,
            kernel_size=self.kernel_size,
            padding="same",
            activation=tf.nn.relu)

        # # Pool Layer 2 nd reshape images by 2
        pool2 = tf.layers.max_pooling2d(inputs=convolution_2, pool_size=[2, 2], strides=2)
        # Dense Layer
        # TODO Checks max pools numbers
        pool2_flat = tf.reshape(pool2, [-1, int(self._input_rows_numbers / 4) * int(self._input_columns_numbers / 4)
                                        * self.third_label_neurons])
        dense = tf.layers.dense(inputs=pool2_flat, units=self.third_label_neurons, activation=tf.nn.relu)
        dropout = tf.nn.dropout(dense, keep_probably)
        # Readout Layer
        w_fc2 = weight_variable([self.third_label_neurons, self.number_of_classes])
        b_fc2 = bias_variable([self.number_of_classes])
        y_convolution = (tf.matmul(dropout, w_fc2) + b_fc2)

        # Evaluate model
        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=y_,
                                                    logits=y_convolution))  # Cross entropy between y_ and y_conv

        # train_step = tf.train.AdadeltaOptimizer(learning_rate).minimize(cross_entropy)  # Adadelta Optimizer
        train_step = tf.train.AdamOptimizer(self.learning_rate).minimize(
            cross_entropy)  # Adam Optimizer (gradient descent)  # 97-98 test
        # train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)  # Adam Optimizer
        # Sure is axis = 1
        correct_prediction = tf.equal(tf.argmax(y_convolution, axis=1),
                                      tf.argmax(y_, axis=1))  # Get Number of right values in tensor
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  # Get accuracy in float

        options = [Dictionary.string_option_signals_images_problem,cv2.IMREAD_GRAYSCALE,
                   self.input_rows_columns_array[0],self.input_rows_columns_array[1]]
        # Batching values and labels from input and labels (with batch size)
        x_batch_feed, label_batch_feed = self.data_buffer_generic_class(inputs=self.input,
                                                                        inputs_labels=self.input_labels,
                                                                        shuffle_data=self.shuffle_data,
                                                                        batch_size=self.batch_size,
                                                                        options=options)
        x_test_feed, y_test_feed = process_test_set(self.test,self.test_labels,options)

        # Session
        sess = tf.InteractiveSession()
        sess.run(tf.local_variables_initializer())
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()

        start_time = time.time()
        # TRAIN
        for epoch in range(self.epoch_numbers):
            for i in range(self.trains):
                # Setting values
                feed_dict_train_50 = {x: x_batch_feed, y_: label_batch_feed, keep_probably: self.train_dropout}
                feed_dict_train_100 = {x: x_batch_feed, y_: label_batch_feed, keep_probably: 1}
                feed_dict_test_100 = {x: x_test_feed, y_: y_test_feed, keep_probably: 1}
                train_accuracy = accuracy.eval(feed_dict_train_100) * 100
                train_step.run(feed_dict_train_50)
                test_accuracy = accuracy.eval(feed_dict_test_100) * 100

                cross_entropy_train = cross_entropy.eval(feed_dict_train_100)
                '''
                if test_accuracy > 99:
                    # TODO return best previous model to check when save new model
                    # Save the variables to disk.
                    save_path = saver.save(sess, "/tmp/model.ckpt")
                    # TODO Write in text file new models with features
                '''

                # TODO Use validation set
                if self.show_info:

                    y__ = y_.eval(feed_dict_train_100)
                    argmax_labels_y_ = [np.argmax(m) for m in y__]
                    pt('y__shape', y__.shape)
                    pt('argmax_labels_y__', argmax_labels_y_)
                    pt('y__[-1]', y__[-1])

                    y__conv = y_convolution.eval(feed_dict_train_100)
                    argmax_labels_y_convolutional = [np.argmax(m) for m in y__conv]
                    pt('argmax_y_conv', argmax_labels_y_convolutional)
                    pt('y_conv_shape', y__conv.shape)
                    pt('index_buffer_data', self.index_buffer_data)

                if i == 0 or i % 10 == 0:
                    clear_console()
                    percent_advance = str(i * 100 / self.trains)
                    pt('Seconds', (time.time() - start_time))
                    pt('Time', str(time.strftime("%Hh%Mm%Ss", time.gmtime((time.time() - start_time)))))
                    pt('TRAIN NUMBER: ' + str(self.num_trains_count + 1) + ' | Percent Epoch ' + str(
                        epoch + 1) + ": " + percent_advance + '%')
                    pt('train_accuracy', train_accuracy)
                    pt('cross_entropy_train', cross_entropy_train)
                    pt('test_accuracy', test_accuracy)
                    pt('self.index_buffer_data',self.index_buffer_data)
                self.num_trains_count += 1
                # Update batches values
                x_batch_feed, label_batch_feed = self.data_buffer_generic_class(inputs=self.input,
                                                                                inputs_labels=self.input_labels,
                                                                                shuffle_data=self.shuffle_data,
                                                                                batch_size=self.batch_size,
                                                                                options=options)
        pt('END TRAINING ')

    def update_inputs_and_labels_shuffling(self, inputs, inputs_labels):
        """
        Update inputs_processed and labels_processed variables with an inputs and inputs_labels shuffled

        :param inputs: Represent input data
        :param inputs_labels:  Represent labels data
        """
        c = list(zip(inputs, inputs_labels))
        random.shuffle(c)
        self.inputs_processed, self.labels_processed = zip(*c)

    def data_buffer_generic_class(self,inputs, inputs_labels, shuffle_data, batch_size, options=None):
        """
        Create a data buffer having necessaries class attributes (inputs,labels,...)
        :param shuffle_data: If it is necessary shuffle data.
        :param batch_size: The batch size .
        :param is_test: if the inputs are the test set.
        :return: Two numpy arrays (x_batch and y_batch) with input data and input labels data batch_size like shape.
        """
        x_batch = []
        y_batch = []
        if shuffle_data and self.index_buffer_data == 0:
            self.input, self.input_labels = get_inputs_and_labels_shuffled(self.input,self.input_labels)
            pt("SHUFLLEDDDDDDDDDDDDDDDDDDDDDDD")
        batch_size, out_range = self.get_out_range_and_batch()  # out_range will be True if next batch is out of range
        for _ in range(batch_size):
            x, y = process_input_unity_generic(self.input[self.index_buffer_data],
                                               self.input_labels[self.index_buffer_data],
                                               options)
            x_batch.append(x)
            y_batch.append(y)
            self.index_buffer_data += 1
        x_batch = np.asarray(x_batch)
        y_batch = np.asarray(y_batch)
        if out_range:  # Reset index_buffer_data
            self.index_buffer_data = 0
        return x_batch, y_batch

    def get_out_range_and_batch(self):
        """
        Return out_range flag and new batch_size if necessary. It is necessary when batch is bigger than input rest of
        self.index_buffer_data
        :return: out_range (True or False), batch_size (int)
        """
        out_range = False
        batch_size = self.batch_size
        if self.input_size - self.index_buffer_data == 0:  # When is all inputs
            out_range = True
        elif self.input_size - self.index_buffer_data < self.batch_size:
            batch_size = self.input_size - self.index_buffer_data
            out_range = True
        return batch_size, out_range

"""
STATIC METHODS
"""

def get_inputs_and_labels_shuffled(inputs, inputs_labels):
    """
    Get inputs_processed and labels_processed variables with an inputs and inputs_labels shuffled
    :param inputs: Represent input data
    :param inputs_labels:  Represent labels data
    :returns inputs_processed, labels_processed
    """
    c = list(zip(inputs, inputs_labels))
    random.shuffle(c)
    inputs_processed, labels_processed = zip(*c)
    return inputs_processed, labels_processed

def process_input_unity_generic(x_input, y_label, options=None):
    """
    Generic method that process input and label across a if else statement witch contains a string that represent
    the option (option = how process data)
    :param x_input: A single input
    :param y_label: A single input label 
    :param options: All attributes to process data. First position must to be the option.
    :return: x_input and y_label processed
    """
    if options:
        option = options[0]  # Option selected
        if option == Dictionary.string_option_signals_images_problem:
            x_input = process_image_signals_problem(x_input,options[1],options[2],options[3])

    return x_input, y_label

# noinspection PyUnresolvedReferences
def process_image_signals_problem(image, image_type, height, width):
    """
    :param image: The image to change
    :param image_type: Gray Scale, RGB, HSV
    :return:
    """
    # 1- Get image in GrayScale
    # 2- Modify intensity and contrast
    # 3- Transform to gray scale
    # 4- Return image
    image = cv2.imread(image, image_type)
    image = cv2.resize(image, (height, width))
    image = cv2.equalizeHist(image)
    image = cv2.equalizeHist(image)
    random_percentage = random.randint(3, 20)
    to_crop_height = int((random_percentage * height) / 100)
    to_crop_width = int((random_percentage * width) / 100)
    image = image[to_crop_height:height - to_crop_height, to_crop_width:width - to_crop_width]
    image = cv2.copyMakeBorder(image, top=to_crop_height,
                                   bottom=to_crop_height,
                                   left=to_crop_width,
                                   right=to_crop_width,
                                   borderType=cv2.BORDER_CONSTANT)
    image = image.reshape(-1)
    # cv2.imshow('image', image)
    # cv2.waitKey(0)  # Wait until press key to destroy image
    return image


def process_test_set(test, test_labels, options):
    x_test = []
    y_test = []
    for i in range(len(test)):
        x, y = process_input_unity_generic(test[i],test_labels[i],options)
        x_test.append(x)
        y_test.append(y)
    x_test = np.asarray(x_test)
    y_test = np.asarray(y_test)
    return x_test, y_test

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    #initial = tf.zeros(shape, dtype=tf.float32)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.01, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')

def number_neurons(total_input_size, input_sample_size, output_size, alpha=1):
    """
    :param total_input_size: x
    :param input_sample_size: x
    :param output_size: x
    :param alpha: x
    :return: number of neurons for layer
    """
    return int(total_input_size/(alpha*(input_sample_size+output_size)))
