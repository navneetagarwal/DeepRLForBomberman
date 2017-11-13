# from keras.models import Sequential
# from keras.layers import Dense, Activation
# from keras.utils.vis_utils import plot_model
from modelConf import modelConf
import tensorflow as tf
import numpy as np
import os

class network:
	def __init__(self, gamma):
		# Get the model configuration
		self.conf = modelConf()
		self.inputDim = self.conf.numInputs
		self.outputDim = self.conf.numOutputs

		# Gamma for RL in the agent
		self.gamma = gamma
		tf.reset_default_graph()
		#These lines establish the feed-forward part of the network used to choose actions
		layers = []
		self.inp = tf.placeholder(shape=[1,self.inputDim], dtype=tf.float32)
		layers.append(self.inp)
		
		for i in range(self.conf.numLayers):	
			# Add fully connected layerS
			# Add activation
			if (self.conf.activations[i] == 'relu'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=self.conf.outputs[i], activation=tf.nn.relu, name="layer"+str(i)))
			elif(self.conf.activations[i] == 'tanh'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=self.conf.outputs[i], activation=tf.nn.tanh, name="layer"+str(i)))
			elif(self.conf.activations[i] == 'sigmoid'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=self.conf.outputs[i], activation=tf.nn.sigmoid, name="layer"+str(i)))
			elif(self.conf.activations[i] == 'softmax'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=self.conf.outputs[i], activation=tf.nn.softmax, name="layer"+str(i)))
			else:
				layers.append(tf.layers.dense(inputs=layers[-1], units=self.conf.outputs[i], activation=None, name="layer"+str(i)))

		self.Q = layers[-1]

		#We will provide the next Q from the training function
		self.optimalQ = tf.placeholder(shape=[1,self.outputDim], dtype=tf.float32)
		self.loss = tf.reduce_sum(tf.square(self.optimalQ - self.Q))
		trainer = tf.train.GradientDescentOptimizer(learning_rate=self.conf.lr)
		self.backProp = trainer.minimize(self.loss)

	def _startSess(self, loadModel):
		self.sess = tf.Session()

		if not loadModel:
			self.sess.run(tf.global_variables_initializer())
		else:
			saver = tf.train.Saver()
			saver.restore(self.sess, "../models/model.ckpt")

	def findQ(self, state):
		return(self.sess.run(self.Q, feed_dict={self.inp: state}))

	def trainNetwork(self, state, action, reward, nextState):
		Q = self.findQ(state)		
		nextQ = self.findQ(nextState)
		bestVal = np.argmax(nextQ)
		updatedVal = reward + (self.gamma*bestVal)
		
		# Make the optimal Q vector for training
		optimalQ = Q
		optimalQ[0,action] = updatedVal
		loss,_ = self.sess.run([self.loss, self.backProp], feed_dict={self.inp: state, self.optimalQ: optimalQ})
		return loss

	def saveNetwork(self):
		try:
			os.stat('../models')
		except:
			os.mkdir('../models', 0775)
		saver = tf.train.Saver()
		save_path = saver.save(self.sess, "../models/model.ckpt")
  		print("Model saved in file: %s" % save_path)



# # Construct the model
# self.model = Sequential()
# for i in range(self.conf.numLayers):
# 	# Add fully connected layer
# 	if(i==0):
# 		self.model.add(Dense(units=self.conf.outputs[i], input_dim=inputDim))
# 	else:
# 		self.model.add(Dense(units=self.conf.outputs[i]))

# 	# Add activation
# 	if (self.conf.activations[i] == 'relu'):
# 		self.model.add(Activation('relu'))
# 	elif(self.conf.activations[i] == 'tanh'):
# 		self.model.add(Activation('tanh'))
# 	elif(self.conf.activations[i] == 'sigmoid'):
# 		self.model.add(Activation('sigmoid'))
# 	elif(self.conf.activations[i] == 'softmax'):
# 		self.model.add(Activation('softmax'))

# # Visualize the model
# plot_model(self.model, to_file='model.png')