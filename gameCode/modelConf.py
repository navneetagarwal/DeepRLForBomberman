class modelConf:
	def __init__(self):
		self.numLayers 		= 2
		self.numInputs		= 21
		self.numOutputs		= 6
		self.outputs 		= [50, 6]
		self.activations 	= ['sigmoid', 'softmax']
		self.lr 			= 0.01

		assert (self.numLayers == len(self.outputs)), "Incompatible Model Specification"
		assert (self.numOutputs == self.outputs[-1]), "Incompatible Output Dimensions in model specification"
