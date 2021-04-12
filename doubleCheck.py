def ensure_dir(file_path):
	directory = os.path.realpath(file_path)
	if not os.path.exists(directory):
		print('Creating directory: ' + os.path.basename(directory))
		os.makedirs(directory)

def confirmDB(state, plate):
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	prompt = " [y/n] "

	while True:
		print("Add " + state + ":" + plate + " to database? " + prompt)
		#sys.stdout.write(question + prompt)
		choice = input().lower()

		if choice in valid:
			return valid[choice]
		else:
			print("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")