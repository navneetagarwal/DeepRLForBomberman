from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils.vis_utils import plot_model
from modelConf import modelConf

class network:
	def __init__(self, gamma):
		# Get the model configuration
		self.conf = modelConf()
		self.inputDim = conf.numInputs
		self.outputDim = conf.outputDim

		# Gamma for RL in the agent
		self.gamma = gamma

		#These lines establish the feed-forward part of the network used to choose actions
		layers = []
		self.inp = tf.placeholder(shape=[1,self.inputDim], dtype=tf.float32)
		layers.append[self.inp]
		
		for i in range(conf.numLayers):	
			# Add fully connected layerS
			# Add activation
			if (conf.activations[i] == 'relu'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=conf.outputs[i], activation=tf.nn.relu, name="layer "+str(i)))
			elif(conf.activations[i] == 'tanh'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=conf.outputs[i], activation=tf.nn.tanh, name="layer "+str(i)))
			elif(conf.activations[i] == 'sigmoid'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=conf.outputs[i], activation=tf.nn.sigmoid, name="layer "+str(i)))
			elif(conf.activations[i] == 'softmax'):
				layers.append(tf.layers.dense(inputs=layers[-1], units=conf.outputs[i], activation=tf.nn.softmax, name="layer "+str(i)))
			else:
				layers.append(tf.layers.dense(inputs=layers[-1], units=conf.outputs[i], activation=None, name="layer "+str(i)))

		self.Q = layers[-1]

		#We will provide the next Q from the training function
		self.optimalQ = tf.placeholder(shape=[1,self.outputDim], dtype=tf.float32)
		self.loss = tf.reduce_sum(tf.square(self.optimalQ - self.Q))
		trainer = tf.train.GradientDescentOptimizer(learning_rate=conf.lr)
		self.backProp = trainer.minimize(self.loss)

	def _startSess(self):
		self.sess = tf.Session()
		self.sess.run(tf.initialize_all_variables())

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
		loss,_ = sess.run([self.loss, self.backProp], feed_dict={self.inp: state, self.optimalQ: optimalQ})
		return loss



# # Construct the model
# self.model = Sequential()
# for i in range(conf.numLayers):
# 	# Add fully connected layer
# 	if(i==0):
# 		self.model.add(Dense(units=conf.outputs[i], input_dim=inputDim))
# 	else:
# 		self.model.add(Dense(units=conf.outputs[i]))

# 	# Add activation
# 	if (conf.activations[i] == 'relu'):
# 		self.model.add(Activation('relu'))
# 	elif(conf.activations[i] == 'tanh'):
# 		self.model.add(Activation('tanh'))
# 	elif(conf.activations[i] == 'sigmoid'):
# 		self.model.add(Activation('sigmoid'))
# 	elif(conf.activations[i] == 'softmax'):
# 		self.model.add(Activation('softmax'))

# # Visualize the model
# plot_model(self.model, to_file='model.png')