import sys
import argparse

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--algorithm', 	choices=["random", "reflex", "DeepQ"], default="DeepQ", help='Which Algorithm to Use')
	parser.add_argument('--epochs', type=int, default=1, help='Choose the number of epochs')
	parser.add_argument('--isLoad', action="store_true", default=False, help='Load Model')
	parser.add_argument('--isSave', action="store_true", default=False, help='Store Model')
	parser.add_argument('--graphics', action="store_true", default=False, help='Which Algorithm to Use')
	parser.add_argument('--isTest', action="store_true", default=False, help='Testing Phase')
	parser.add_argument('--eps', type=float, default=0.5, help='Epsilon for E-Greedy strategy')
	args = parser.parse_args()
	# print args.eps
	import titlescreen
	
	t = titlescreen.Titlescreen(args.algorithm, args.epochs, args.isLoad, args.isSave, args.graphics, args.eps, args.isTest)
