class modelConf:
	def __init__(self):
		self.numLayers 		= 3
		self.numInputs		= 20
		self.outputs 		= [10, 10, 4]
		self.activations 	= ['relu', 'relu', 'softmax']

		assert (self.numLayers == len(self.outputs)), "Incompatible Model Specification"
