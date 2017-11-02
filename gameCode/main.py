import titlescreen, sys

if __name__ == "__main__":
	playerAlgo = sys.argv[1]	
	epochs = sys.argv[2]
	t = titlescreen.Titlescreen(playerAlgo, epochs)
