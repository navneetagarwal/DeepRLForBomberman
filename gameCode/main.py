import titlescreen, sys

if __name__ == "__main__":

	if len(sys.argv) != 3:
		sys.stdout.write("Incorrect Usage: (Number of arguments = 2)\n\tArg 1 -> Agent algorithm (eg. random, reflex, etc.)\n\tArg 2 -> Number of epochs (eg. 1, 2, etc.)\n")
		exit()

	playerAlgo = sys.argv[1]	
	epochs = sys.argv[2]
	t = titlescreen.Titlescreen(playerAlgo, epochs)
