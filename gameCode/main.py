import sys

if __name__ == "__main__":

	if len(sys.argv) != 5:
		sys.stdout.write("Incorrect Usage: (Number of arguments = 4)\n \
			Arg 1 -> Agent algorithm (eg. random, reflex, etc.)\n \
			Arg 2 -> Number of epochs (eg. 1, 2, etc.)\n \
			Arg 3 -> 0 - Dont Load 1 - Load Model\n \
			Arg 4 -> 0 - Dont Save 1 - Save Model\n")
		exit()

	import titlescreen
	
	playerAlgo = sys.argv[1]	
	epochs = int(sys.argv[2])
	isLoad = int(sys.argv[3])
	isSave = int(sys.argv[4])

	t = titlescreen.Titlescreen(playerAlgo, epochs, isLoad, isSave)
