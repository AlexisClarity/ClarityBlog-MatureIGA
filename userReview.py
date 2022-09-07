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

import json
import xlsxwriter

def collectIdentitiesFromJson(fileName, managers):

	with open(fileName, 'r') as file:
		identityData = json.load(file)

		for key in identityData:
			manager = identityData[key][5]
			print(manager)

			if isinstance(manager, list):
				x = 0
				while x < len(manager):
					if manager[x] not in managers.keys():
						managers[manager[x]] = [identityData[key][0:5] + identityData[key][6:]]
					else:
						managers[manager[x]].append(identityData[key][0:5] + identityData[key][6:])
					x = x + 1
			else: 
				if manager not in managers.keys():
					managers[manager] = [identityData[key][0:5] + identityData[key][6:]]
				else:
					managers[manager[x]].append(identityData[key][0:5] + identityData[key][6:])

	return managers

def writeManagerReviews(managers):

	headerNames = ["Full Name", "First Name", "Last Name", "Email", 
		"Application", "User Creation Date", 
		"User Account Status", "Other", "Manager Response (Drop Down)"]
	dataValidation = ['Employed', 'Terminated', 'Changed Teams', 'Do Not Recognize']

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
			
			dVCell = 'I' + str(row+1)
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

def managersToJson(managers):

	json_object = json.dumps(managers, indent=4)
	with open("managers.json", 'w') as jsonFile:
		jsonFile.write(json_object)

def main():

	managers = {}
	fileName = "IdentityInventory.json"

	managers = collectIdentitiesFromJson(fileName, managers)

	writeManagerReviews(managers)
	managersToJson(managers)
	
main()
