import csv

def collectFileNames():

	fileNames = []
	numberOfFiles = int(input('\nHow many files are in scope? (INTEGERS ONLY) '))
	x = 0
	while x < numberOfFiles:
		fileName = input('\nWhat is the name of file %s? (Include extension and path if script is not in the same directory) ' %(x+1))
		fileNames.append(fileName)
		x = x + 1
	return fileNames

def csvEvaluation(file, identities):

	headerNames = {1:"Full Name", 2: "First Name", 3:"Last Name", 4:"Email", 
		5:"Application", 6:"Manager", 7:"User Creation Date", 
		8:"User Account Status", 9:"Other"
	}
	headers = {}
	with open(file) as csvFile:
		contentReader = csv.reader(csvFile, delimiter = ',')
		firstRow = next(contentReader)
		x = 0

		print(headerNames)
		print("Using 1 - 9, let's identify the contents of each column! \n")
		
		for column in firstRow:
			columnContents = int(input('What are the contents of column %s? -- %s:  ' %(x+1, column)))
			headers[columnContents] = x
			x = x + 1

		for row in contentReader:
			fullName = ""
			if 1 in headers.keys():
				fullName = row[headers[1]]
			elif 2 in headers.keys() and 3 in headers.keys():
				fullName = row[headers[2]] + " " + row[headers[3]]
			else: 
				print("there is no full name, exiting")
				return
			y = 1

			if fullName in identities.keys():
				try: 
					if isinstance(identities[fullName][5],list):
						identities[fullName][5].append(row[headers[5]])
					else:
						identities[fullName][5] = [identities[fullName][5], row[headers[5]]]
				except:
					pass
				y = 1000000000
			else: 
				identities[fullName] = []
			while y < 10: 
				try:
					identities[fullName].append(row[headers[y]])
				except:
					identities[fullName].append("-")
				y = y + 1
	return identities


def main():
	identities = {}
	managers = {}
	fileNames = collectFileNames()
	for file in fileNames:
		csvEvaluation(file, identities)

	headerNames = ["Full Name", "First Name", "Last Name", "Email", 
		"Application", "Manager", "User Creation Date", 
		"User Account Status", "Other"]

	with open("userReview.csv", 'w', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(headerNames)

		for key in identities.keys():
			writer.writerow(identities[key])

	print(identities)

	for key in identities.keys():
		try:
			managers[identities[key][5]].append(identities[key])
		except:
			managers[identities[key][5]] = identities[key]

	for key in managers.keys():
		file = key + ".csv"
		with open(file, 'w', newline='') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(headerNames)
			for row in managers[key]:
				writer.writerow(row)

main()