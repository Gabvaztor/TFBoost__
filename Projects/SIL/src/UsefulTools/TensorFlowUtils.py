# -*- coding: utf-8 -*-
import tensorflow as tf

def weighted_mape_tf(y_true, y_prediction):
    tot = tf.reduce_sum(y_true)
    wmape = tf.truediv(tf.reduce_sum(tf.abs(tf.subtract(y_true, y_prediction))), tot)
    return wmape


def root_mean_squared_logarithmic_error(y_true, y_prediction):
    """
    Calculate the Root Mean Squared Logarithmic Error
    :param y_true: y_logits
    :param y_prediction: y_prediction
    :return: Root Mean Squared Logarithmic Error
    """
    # TODO (@gabvaztor) Do Root Mean Squared Logarithmic Error
    pass


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    # initial = tf.zeros(shape, dtype=tf.float32)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.truncated_normal(shape=shape, stddev=0.01)
    return tf.Variable(initial)


def conv2d(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


def initialize_session(debug_level=None):
    """
    Initialize interactive session and all local and global variables
    :return: Session
    """
    if debug_level == 3 or debug_level == 2 or debug_level == 1 :
        config = tf.ConfigProto(allow_soft_placement=True,
                                log_device_placement=True)
    else:
        config = tf.ConfigProto(allow_soft_placement=True)
    sess = tf.InteractiveSession(config=config)
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())
    return sess
