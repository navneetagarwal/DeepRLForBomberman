from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils.vis_utils import plot_model
from modelConf import modelConf

class network:
def __init__(self):
	# Get the model configuration
	self.conf = modelConf()
	self.inputDim = conf.numInputs

	# Construct the model
	self.model = Sequential()
	for i in range(conf.numLayers):
		# Add fully connected layer
		if(i==0):
			self.model.add(Dense(units=conf.outputs[i], input_dim=inputDim))
		else:
			self.model.add(Dense(units=conf.outputs[i]))

		# Add activation
		if (conf.activations[i] == 'relu'):
			self.model.add(Activation('relu'))
		elif(conf.activations[i] == 'tanh'):
			self.model.add(Activation('tanh'))
		elif(conf.activations[i] == 'sigmoid'):
			self.model.add(Activation('sigmoid'))
		elif(conf.activations[i] == 'softmax'):
			self.model.add(Activation('softmax'))

	# Visualize the model
	plot_model(self.model, to_file='model.png')