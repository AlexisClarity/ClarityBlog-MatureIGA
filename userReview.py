import json
import xlsxwriter

def collectIdentitiesFromCsv(fileName, managers):

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

def main():

	managers = {}
	fileName = "IdentityInventory.json"

	managers = collectIdentitiesFromCsv(fileName, managers)

	writeManagerReviews(managers)
	
main()
