class modelConf:
	def __init__(self):
		self.numLayers 		= 3
		self.numInputs		= 37
		self.numOutputs		= 6
		self.outputs 		= [40, 40, 6]
		self.activations 	= ['relu', 'relu', 'softmax']
		self.lr 			= 0.01

		assert (self.numLayers == len(self.outputs)), "Incompatible Model Specification"
		assert (self.numOutputs == self.outputs[-1]), "Incompatible Output Dimensions in model specification"
