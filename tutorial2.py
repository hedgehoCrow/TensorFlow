# coding: UTF-8

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

# 畳み込み層、プーリング層その1
w1 = tf.Variable(tf.truncated_normal([5,5,1,32], stddev=0.1))
b1 = tf.Variable(0.1, [32])
x_image = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(tf.nn.conv2d(x_image, w1, strides=[1,1,1,1], padding='SAME')+b1)
h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

# 畳み込み層、プーリング層その2
w2 = tf.Variable(tf.truncated_normal([5,5,32,64], stddev=0.1))
b2 = tf.Variable(0.1, [64])

h_conv2 = tf.nn.relu(tf.nn.conv2d(h_pool1, w2, strides=[1,1,1,1], padding='SAME')+b2)
h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

W_fc1 = tf.Variable(tf.truncated_normal([7*7*64,1024], stddev=0.1))
b_fc1 = tf.Variable(0.1, [1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# 読み出し層
W_fc2 = tf.Variable(tf.truncated_normal([1024,10], stddev=0.1))
b_fc2 = tf.Variable(0.1, [10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# モデル学習、評価
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.initialize_all_variables())

#for i in range(20000):
for i in range(1500):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print ("step %d, training accuracy %g" % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
        
print ("test accuracy %g" % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))







