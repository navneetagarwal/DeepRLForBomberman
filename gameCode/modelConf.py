class modelConf:
	def __init__(self):
		self.numLayers 		= 2
		self.numInputs		= 16
		self.numOutputs		= 1
		self.outputs 		= [24, 1]
		self.activations 	= ['tanh', 'tanh']
		self.lr 			= 0.01

		assert (self.numLayers == len(self.outputs)), "Incompatible Model Specification"
		assert (self.numOutputs == self.outputs[-1]), "Incompatible Output Dimensions in model specification"
