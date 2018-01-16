# note class called for graphics
# contains all possible draw methods for notes
# including quarter, half, whole, and sharp
# and different properties of notes

import math
from keys import *
from tkinter import *

class Note(object):
	
	def __init__(self,frequency):
		self.frequency=frequency
		self.r=10
		self.visible=True
		self.length=1
		self.sharp=False

	def findKey(self,dft):
		min=dft.framerate+1 #frequency cannot be this high
		note="C4" #base note initialized to
		for key in keys:
			#map frequency to key
			diff=abs(key-self.frequency)
			if diff<=min:
				min=diff
				note=keys[key]
		self.key=note
		if "." in self.key:
			self.sharp=True
		self.line=keyLines[note]


	def drawTrebleQuarter(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,
			((line-1)*data.dy//2)+data.margin-data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,
			((line-1)*data.dy//2)+data.margin+data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,
			fill="#000000")
		canvas.create_line(cx+data.noteR,
			((line-1)*data.dy//2)+data.margin+(staffNum*data.staffMargin*2)\
			-data.scrollY,
			cx+data.noteR,
			((line-1)*data.dy//2)+data.margin*data.goldenRatio+\
			(staffNum*data.staffMargin*2)-data.scrollY)

	def drawCQuarter(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,((line-1)*data.dy//2)+data.margin-\
		data.noteR+(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,((line-1)*data.dy//2)+data.margin+data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,fill="#000000")
		canvas.create_line(cx-data.noteR*2,((line-1)*data.dy//2)+data.margin+\
		(staffNum*data.staffMargin*2)-data.scrollY,
				cx+data.noteR*2,((line-1)*data.dy//2)+data.margin+\
				(staffNum*data.staffMargin*2)-data.scrollY,width=1)
		canvas.create_line(cx+data.noteR,((line-1)*data.dy//2)+data.margin+\
		(staffNum*data.staffMargin*2)-data.scrollY,
				cx+data.noteR,((line-1)*data.dy//2)+data.margin*\
				data.goldenRatio+(staffNum*data.staffMargin*2)-data.scrollY)

	def drawBassQuarter(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,
		((line-3)*data.dy//2)+data.margin-data.noteR+data.staffMargin//2+\
		(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,((line-3)*data.dy//2)+data.margin+data.noteR+\
			data.staffMargin//2+(staffNum*data.staffMargin*2)-data.scrollY,
			fill="#000000")
		canvas.create_line(cx-data.noteR,((line-3)*data.dy//2)+data.margin+\
		data.staffMargin//2+(staffNum*data.staffMargin*2)-data.scrollY,
				cx-data.noteR,((line-3)*data.dy//2)+data.margin*\
				data.goldenRatio*2+data.staffMargin*data.goldenRatio\
				+(staffNum*data.staffMargin*2)-data.scrollY)



	def drawTrebleHalf(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,((line-1)*data.dy//2)+data.margin-\
		data.noteR+(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,((line-1)*data.dy//2)+data.margin+data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,fill="#ffffff",width=1)
		canvas.create_line(cx+data.noteR,((line-1)*data.dy//2)+data.margin+\
		(staffNum*data.staffMargin*2)-data.scrollY,
				cx+data.noteR,
				((line-1)*data.dy//2)+data.margin*data.goldenRatio+\
				(staffNum*data.staffMargin*2)-data.scrollY)

	def drawCHalf(self,canvas,data,cx,staffNum,line):
		canvas.create_line(cx+data.noteR,((line-1)*data.dy//2)+data.margin+\
		(staffNum*data.staffMargin*2)-data.scrollY,
				cx+data.noteR,((line-1)*data.dy//2)+data.margin*\
				data.goldenRatio+(staffNum*data.staffMargin*2)-data.scrollY)
		canvas.create_line(cx-data.noteR*2,((line-1)*data.dy//2)+data.margin+\
		(staffNum*data.staffMargin*2)-data.scrollY,
				cx+data.noteR*2,((line-1)*data.dy//2)+data.margin+\
				(staffNum*data.staffMargin*2)-data.scrollY,width=1)
		canvas.create_oval(cx-data.noteR,((line-1)*data.dy//2)+data.margin-\
		data.noteR+(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,
			((line-1)*data.dy//2)+data.margin+data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,fill="#ffffff",width=1)


	def drawBassHalf(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,((line-3)*data.dy//2)+data.margin-\
		data.noteR+data.staffMargin//2+(staffNum*data.staffMargin*2)-\
		data.scrollY,
			cx+data.noteR,((line-3)*data.dy//2)+data.margin+data.noteR+\
			data.staffMargin//2+(staffNum*data.staffMargin*2)-data.scrollY,\
			fill="#ffffff",width=1)
		canvas.create_line(cx-data.noteR,((line-3)*data.dy//2)+data.margin+\
		data.staffMargin//2+(staffNum*data.staffMargin*2)-data.scrollY,
				cx-data.noteR,((line-3)*data.dy//2)+data.margin*\
				data.goldenRatio*2+data.staffMargin*data.goldenRatio+\
				(staffNum*data.staffMargin*2)-data.scrollY)


	def drawTrebleWhole(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,((line-1)*data.dy//2)+data.margin-\
		data.noteR+(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,((line-1)*data.dy//2)+data.margin+data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,fill="#ffffff",width=1)

	def drawCWhole(self,canvas,data,cx,staffNum,line):
		canvas.create_line(cx-data.noteR*2,((line-1)*data.dy//2)+data.margin+\
		(staffNum*data.staffMargin*2)-data.scrollY,
				cx+data.noteR*2,((line-1)*data.dy//2)+data.margin+\
				(staffNum*data.staffMargin*2)-data.scrollY,width=1)
		canvas.create_oval(cx-data.noteR,((line-1)*data.dy//2)+data.margin-\
		data.noteR+(staffNum*data.staffMargin*2)-data.scrollY,
			cx+data.noteR,((line-1)*data.dy//2)+data.margin+data.noteR+\
			(staffNum*data.staffMargin*2)-data.scrollY,fill="#ffffff",width=1)
	

	def drawBassWhole(self,canvas,data,cx,staffNum,line):
		canvas.create_oval(cx-data.noteR,((line-3)*data.dy//2)+data.margin-\
		data.noteR+data.staffMargin//2+(staffNum*data.staffMargin*2)-\
		data.scrollY,
			cx+data.noteR,((line-3)*data.dy//2)+data.margin+data.noteR+\
			data.staffMargin//2+(staffNum*data.staffMargin*2)-data.scrollY,
			fill="#ffffff",width=1)
		

	def drawSharp(self,canvas,data,cx,staffNum,line):
		if line <=10:
			canvas.create_text(cx-data.noteR,
				((line-1)*data.dy//2)+data.margin+(staffNum*data.staffMargin*2)\
				-data.scrollY,
				text="#",anchor=E,fill="#000000", font="Helvetica %d bold" \
				%(data.fontSize))
		elif line==11:
			canvas.create_text(cx-data.noteR,((line-1)*data.dy//2)+\
			data.margin+(staffNum*data.staffMargin*2)-data.scrollY,
				text="#",anchor=E,fill="#000000", font="Helvetica %d bold"\
				 %(data.fontSize))
		else:
			canvas.create_text(cx-data.noteR,((line-3)*data.dy//2)+\
			data.margin+data.staffMargin//2+(staffNum*data.staffMargin*2)-\
			data.scrollY,
				text="#",anchor=E,fill="#000000", font="Helvetica %d bold" \
				%(data.fontSize))



	def drawNote(self,canvas,data,cx,staffNum,line):
		#call draw method on notes,
		#stratifying by length of note and sharp/natural
		if self.visible:
			if self.length==1:
				if line<=10: #treble cleff/top staff
					self.drawTrebleQuarter(canvas,data,cx,staffNum,line)
				elif line==11: #middle C
					self.drawCQuarter(canvas,data,cx,staffNum,line)
				else:
					self.drawBassQuarter(canvas,data,cx,staffNum,line)
			elif self.length==2:
				if line<=10: #treble cleff/top staff
					self.drawTrebleHalf(canvas,data,cx,staffNum,line)
				elif line==11: #middle C
					self.drawCHalf(canvas,data,cx,staffNum,line)
				else:
					self.drawBassHalf(canvas,data,cx,staffNum,line)
			elif self.length==4:
				if line<=10: #treble cleff/top staff
					self.drawTrebleWhole(canvas,data,cx,staffNum,line)
				elif line==11: #middle C
					self.drawCWhole(canvas,data,cx,staffNum,line)
				else:
					self.drawBassWhole(canvas,data,cx,staffNum,line)
			if "." in self.key:
				self.drawSharp(canvas,data,cx,staffNum,line)


	def __repr__(self):
		return ("%s,%2f"%(self.key,self.frequency))


	def __eq__(self,other):
		return isinstance(self,other) and self.key==other.key