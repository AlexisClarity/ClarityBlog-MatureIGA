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
import pandas

def readExcelReturnDict(fileName, responseDict):

	sheet = pandas.read_excel(fileName, index_col=None, header=0)
	df = pandas.DataFrame(sheet)
	tempDict = df.to_dict()
	return tempDict

def loadManagerJson(fileName):

	with open(fileName, 'r') as file:
		managerData = json.load(file)
		managerNames = list(managerData.keys())
	return managerNames

def createMasterExcel(managers):

	headerNames = ["Manager/Reviewer", "Full Name", "First Name", "Last Name", "Email", 
		"Application", "User Creation Date", 
		"User Account Status", "Other", "Manager Response"]
	row = 0
	col = 0

	wb = xlsxwriter.Workbook('MasterUserReviewResponse.xlsx')
	worksheet = wb.add_worksheet()
	for header in headerNames:
		worksheet.write(row, col, header)
		col += 1
	mainRow = 1

	for key in managers.keys():
		col = 1
		for subKey in managers[key].keys():
			tempRow = mainRow
			for subSubKey in managers[key][subKey].keys():
				worksheet.write(tempRow, 0, key)
				itemItemToWrite = managers[key][subKey][subSubKey]
				worksheet.write(tempRow, col, itemItemToWrite)
				tempRow += 1
			col += 1
		mainRow = tempRow
	wb.close()

def createSheetsAddHeaders(headerNames, workbook, sheetInfo):

	for sheetName in sheetInfo.keys():
		row = 0
		col = 0
		sheet = workbook.add_worksheet(sheetName)
		for header in headerNames:
			sheet.write(row, col, header)
			col = col + 1

def populateSheet(workbook, sheetName, manager, row, col, content):

	worksheet = workbook.get_worksheet_by_name(sheetName)

	for key in content.keys():
		worksheet.write(row, col, (' & '.join([str(item) for item in content[key]])))
		col += 1

	row += 1
	return row

def createExcel(managers):

	headerNames = ["Full Name", "First Name", "Last Name", "Email", 
		"Application", "User Creation Date", "User Account Status", "Other", "Manager Response (Drop Down)"]
	masterSheetHeaderNames = ["Manager/Reviewer", "Full Name", "First Name", "Last Name", "Email", 
		"Application", "User Creation Date", "User Account Status", "Other", "Manager Response"]
	sheetInfo = {"Master":1, "Conflicting Response":1, "Employed":1, "Terminated":1, "Changed Teams":1, "Do Not Recognize":1}

	userDict = {}
	conflictingResponses = {}


	wb = xlsxwriter.Workbook('MasterUserReviewResponse.xlsx')

	createSheetsAddHeaders(masterSheetHeaderNames, wb, sheetInfo)

	for manager in managers.keys():
		users = managers[manager]["Full Name"].keys()
		for user in users:
			fullName = managers[manager]["Full Name"][user]
			
			if fullName in userDict.keys():
				userDict[fullName]["Manager/Reviewer"].append(manager)
				for header in headerNames:
					if managers[manager][header][user] not in userDict[fullName][header]:
						userDict[fullName][header].append(managers[manager][header][user])
			else:
				userDict[fullName] = {}
				userDict[fullName]["Manager/Reviewer"] = [manager]
				for header in headerNames:
					userDict[fullName][header] = [managers[manager][header][user]]

	for user in userDict.keys():
		if len(userDict[user]["Manager Response (Drop Down)"]) > 1:
			response = userDict[user]["Manager Response (Drop Down)"]
			response = ["Conflicting Response " + ' '.join([str(item) for item in response])]
			userDict[user]["Manager Response (Drop Down)"] = response
			
			mangerName = userDict[user]["Manager/Reviewer"]
			mangerName = ["Multiple Reviewers " + ' '.join([str(item) for item in mangerName])]
			userDict[user]["Manager/Reviewer"] = mangerName
			conflictingResponses[user] = userDict[user]

	for user in userDict.keys():
		manager = userDict[user]["Manager/Reviewer"]
		content = userDict[user]
		page = userDict[user]["Manager Response (Drop Down)"][0]
		print(page)
		
		if user in conflictingResponses.keys():
			sheetInfo["populateSheet"] = populateSheet(wb, "Conflicting Response", manager, sheetInfo["Conflicting Response"], 0, content)
			sheetInfo["Master"] = populateSheet(wb, "Master", manager, sheetInfo["Master"], 0, content)
		else: 
			sheetInfo[page] = populateSheet(wb, page, manager, sheetInfo[page], 0, content)
			sheetInfo["Master"] = populateSheet(wb, "Master", manager, sheetInfo["Master"], 0, content)			




	wb.close()

def main():

	managers = {}
	managerNames = loadManagerJson('managers.json')

	for item in managerNames:
		fileName = item + '.xlsx'
		managers[item] = readExcelReturnDict(fileName, managers)

	createExcel(managers)

main()
