import csv
import xlsxwriter

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
	headers = {1:["Full Name"], 2: ["First Name"], 3:["Last Name"], 4:["Email"], 
		5:["Application"], 6:["Manager"], 7:["User Creation Date"], 
		8:["User Account Status"], 9:["Other"]
	}

	with open(file) as csvFile:
		contentReader = csv.reader(csvFile, delimiter = ',')
		
		#Grabs the first row
		firstRow = next(contentReader)
		
		#Generic iterator
		x = 0

		#Presenting user with instructions
		for key in headers.keys():
			print(key, headers[key][0])

		print("\nUsing 1 - 9, let's identify the contents of each column! \n")
		
		for column in firstRow:
			try:
				columnContents = int(input('What are the contents of column %s? -- %s:  ' %(x+1, column)))
			except:
				print('\n \n \nEnter an integer 1-9\n')
				columnContents = int(input('What are the contents of column %s? -- %s:  ' %(x+1, column)))
			while True:
				if columnContents < 1 or columnContents > 9:
					print('\n \n \nEnter an integer 1-9\n')
					columnContents = int(input('What are the contents of column %s? -- %s:  ' %(x+1, column)))
					continue
				else: 
					break			
			headers[columnContents].append(x)
			x = x + 1

		for row in contentReader:
			
			fullName = ''

			if len(headers[1]) > 1:
				fullName = row[headers[1][1]]
			elif len(headers[2]) > 1 and len(headers[3]) > 1:
				fullName = row[headers[2][1]] + " " + row[headers[3][1]]
			else: 
				print("there is no full name, exiting")
				return

			if fullName not in identities.keys():
				identities[fullName] = []
				for key in headers.keys():
					if len(headers[key]) > 1:
						identities[fullName].append(row[headers[key][1]])
					else:
						identities[fullName].append('-')
			else:

				x = 1
				while x < 10:
					try:
						valueInCsvRow = row[headers[x][1]]
					except:
						valueInCsvRow = '-'
					valueInDict = identities[fullName][x-1]

					if valueInCsvRow == '-' or valueInDict.lower() == valueInCsvRow.lower():
						x = x + 1
						continue
					elif valueInDict == '-':
						identities[fullName][x-1] = valueInCsvRow
					elif valueInCsvRow != valueInDict:
						identities[fullName][x-1] = [valueInDict, valueInCsvRow]

					x = x + 1

	return identities

def managerReviews(identities):

	managers = {}

	for key in identities.keys():
		print(key)
		if isinstance(identities[key][5],list):
			for manager in identities[key][5]:
				if manager in managers.keys():
					managers[manager].append(identities[key])
				else:
					managers[manager] = [identities[key]]
		else:
			manager = identities[key][5]
			if manager in managers.keys():
				managers[manager].append(identities[key])
			else:
				managers[manager] = [identities[key]]

	return managers

def main():
	identities = {}
	managers = {}
	fileNames = collectFileNames()
	for file in fileNames:
		csvEvaluation(file, identities)

	headerNames = ["Full Name", "First Name", "Last Name", "Email", 
		"Application", "Manager", "User Creation Date", 
		"User Account Status", "Other", "Manager Response (Drop Down)"]
	dataValidation = ['Employed', 'Terminated', 'Changed Teams', 'Do Not Recognize']

	#Identity Inventory Writer
	with open("IdentityInventory.csv", 'w', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(headerNames)

		for key in identities.keys():
			writer.writerow(identities[key])

	#Reconstruct the Inventory for manager review
	managers = managerReviews(identities)

	for key in managers.keys():
		row = 0
		col = 0
		wb = xlsxwriter.Workbook(key + '.xlsx')
		worksheet = wb.add_worksheet()

		for header in headerNames:
			worksheet.write(row, col, header)
			col = col + 1
		row = 1
		col = 0

		for rowToWrite in managers[key]:
			for itemItemToWrite in rowToWrite:
				if isinstance(itemItemToWrite, list):
					itemItemToWrite = ' '.join([str(item) for item in itemItemToWrite])
				worksheet.write(row, col, itemItemToWrite)
				col = col + 1
			
			dVCell = 'J' + str(row+1)
			worksheet.data_validation(
				dVCell,
				{
					'validate': 'list',
					'source': dataValidation,
					'input_title': 'Choose One:',
					'input_message': 'Select a value from the list',
				}
			)
			row = row + 1
			col = 0

		wb.close()

main()
