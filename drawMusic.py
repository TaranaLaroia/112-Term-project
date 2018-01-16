#animation file, where sheet music is drawn
#events-example0.py taken from course notes

#pass in fourier transform from analysis file to get dft
#contains init function, keyPressed, and redrawAll

from staff import *
from note import *
from tkinter import *


def init(data,dft):
    data.dy=10
    data.staffMargin=data.dy*10
    data.margin=data.staffMargin
    data.lines=5 #5 lines on a staff
    data.staffs=[]
    data.goldenRatio=0.618 #used to draw stems of piano notes
    data.lineHeight=data.goldenRatio*data.margin
    data.treble=PhotoImage(file="treble.gif")
    data.trebleSize=32
    data.bass=PhotoImage(file="bass.gif")
    data.imgSize=50
    data.frequencies=dft.frequencies
    data.notes=getNotes(data.frequencies,dft)
    data.halfNotes=dft.halfNotes
    data.wholeNotes=dft.wholeNotes
    data.noteR=data.dy//2
    data.dx=30
    data.x=data.dx
    data.lineCapacity=(((data.width-data.margin*2)-data.imgSize)//data.dx)
    data.scrollY=0
    data.scrolldy=20
    data.staffNum=len(data.notes)//(data.lineCapacity)
    for i in range((data.staffNum+1)*2):
        data.staffs.append(Staff(i))
    data.fontSize=data.dx*3//4+1
    data.title=dft.title
    data.titleFont=data.margin//3
    noteLengthCorrection(data)
    

def getNotes(frequencies,dft):
    #map frequencies to notes
    notes=[]
    for frequency in frequencies:
        note=Note(frequency)
        notes.append(note)
        note.findKey(dft)
    return notes

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    #arrow keys scroll window. vertically
    if event.keysym == 'Up':
        if data.scrollY>0:
            data.scrollY-=data.scrolldy
    elif event.keysym =='Down':
        if data.scrollY+data.height<=\
        (len(data.staffs)-1)*data.staffMargin+2*data.margin:
            data.scrollY+=data.scrolldy

def timerFired(data):
    pass


def drawBarlines(canvas,data):
    #outline each silumtaneuos line w/ barlines
    for i in range(data.staffNum+1):
        canvas.create_line(data.margin,
        data.margin-data.scrollY+data.staffMargin*i*2,data.margin,
            data.margin+data.staffMargin+((data.lines-1)*data.dy)\
            -data.scrollY+data.staffMargin*i*2,)
        canvas.create_line(data.width-data.margin,
        data.margin-data.scrollY+data.staffMargin*i*2,data.width-data.margin,
            data.margin+data.staffMargin+((data.lines-1)*data.dy)\
            -data.scrollY+data.staffMargin*i*2,)

def drawClefs(canvas,data):
    #alternate drawing treble/bass clef on every other staff
    for i in range((data.staffNum+1)*2):
        data.staffs[i].drawStaff(canvas,data)
        if i%2==0:
            canvas.create_image(data.margin-data.trebleSize//2,
            data.margin+i*data.staffMargin-data.dy-data.scrollY,
            anchor=NW,image=data.treble)
        else:
            canvas.create_image(data.margin,
            data.margin+i*data.staffMargin-data.scrollY,
            anchor=NW,image=data.bass)

def noteLengthCorrection(data):
    #make notes after half/whole notes invisible
    for i in range(len(data.notes)):
        if i in data.halfNotes:
            data.notes[i].length=2
            try:
                data.notes[i+1].visible=False
            except:
                pass
        if i in data.wholeNotes:
            data.notes[i].length=4
            try:
                data.notes[i+1].visible=False
                data.notes[i+2].visible=False
                data.notes[i+3].visible=False
            except:
                pass

def drawNotes(canvas,data):
    for i in range(len(data.notes)):
        staffNum=(i)//data.lineCapacity
        data.notes[i].drawNote(canvas,data,
        (data.dx*(i%data.lineCapacity)+data.margin+data.noteR+data.imgSize),
        staffNum,data.notes[i].line)

def redrawAll(canvas, data):

    #draw title
    canvas.create_text(data.width//2,data.margin//2-data.scrollY,
    text=data.title,font="Helvetica %d bold" %(data.titleFont),anchor=S)

    drawNotes(canvas,data)
    drawClefs(canvas,data)
    drawBarlines(canvas,data)


def sheetMusic(dft,width=600, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds

    root=Toplevel()

    init(data,dft)
    # create the root and the canvas

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)

    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
