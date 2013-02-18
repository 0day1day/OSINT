import gspread

g = gspread.Client(auth=('xxxxxxxxx','xxxxxxxxxxxx'))
g.login()
worksheet = g.open('TEST').get_worksheet(0)
row = 0
cell = 0


class UpdateSpreadsheet:
	def __init__(self, row, cell, value):
		self.row = row;
		self.cell = cell;
		self.value = value;


aRow = UpdateSpreadsheet(1, 1, "45")
#print(type(aRow.row))
#print(type(aRow.cell))
#print(type(aRow.value))
#row = 1
#cell = 1
#value = '45'
# And then update
#worksheet.update_cell(aRow, aRow.cell, aRow.value)
# First we need to get some cell objects
cell_list = worksheet.range('A1:A7')

print(stocks)
# And finally update them in batch
worksheet.update_cells(cell_list)

#worksheet.update_cell(aRow.row, aRow.cell, aRow.value)
