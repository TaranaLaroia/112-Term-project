# staff class called for graphics
# contains draw method for staffs

class Staff(object):

	def __init__(self,line):
		self.line=line

	def drawStaff(self,canvas,data):
		for i in range(data.lines):
			canvas.create_line(data.margin,
			(self.line*data.staffMargin)+(i*data.dy)+data.margin-data.scrollY,
			data.width-data.margin,
			(self.line*data.staffMargin)+(i*data.dy)+data.margin-data.scrollY,
			width=1)
