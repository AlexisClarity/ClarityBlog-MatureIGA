#Copyright (c) 2022 Clarity Security Corporation

#Permission is hereby granted, free of charge, to any person obtaining a 
#copy of this software and associated #documentation files (the "Software"), 
#to deal in the Software without restriction, including without limitation 
#the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#and/or sell copies of the Software, and to permit persons to whom the 
#Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included 
#in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#DEALINGS IN THE SOFTWARE.


import csv
import xlsxwriter
import json

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

		firstRow = next(contentReader)

		x = 0

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

def main():
	identities = {}
	managers = {}
	fileNames = collectFileNames()
	for file in fileNames:
		csvEvaluation(file, identities)

	headerNames = ["Full Name", "First Name", "Last Name", "Email", 
		"Application", "Manager", "User Creation Date", 
		"User Account Status", "Other"]

	json_object = json.dumps(identities, indent=4)
	with open("IdentityInventory.json", 'w') as jsonFile:
		jsonFile.write(json_object)
	
	#Identity Inventory Writer
	with open("IdentityInventory.csv", 'w', newline='') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(headerNames)

		for key in identities.keys():
			writer.writerow(identities[key])

main()
