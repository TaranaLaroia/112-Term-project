# events-example0.py
# Barebones timer, mouse, and keyboard events

from staff import *
from note import *

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.dy=10
    data.staffMargin=data.dy*10
    data.margin=data.staffMargin
    data.lines=5 #5 lines on a staff
    data.staffs=[]
    #data.staffNum=1
    data.frequencies=[440,278,420,180.3742,700,3432,654,32,54345345,765433,54453,454,3453,454,3,4,4,55345,356,428,4111,3241]
    data.notes=getNotes(data.frequencies)
    data.noteR=data.dy//2
    data.x=0
    data.dx=30
    data.lineCapacity=(data.width-data.margin*2)//data.dx
    #print(data.notes)
    

def getNotes(frequencies):
    notes=[]
    for frequency in frequencies:
        note=Note(frequency)
        notes.append(note)
        note.findKey()
        #print(note)
    return notes

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass



def redrawAll(canvas, data):
    for i in range(len(data.notes)):
        staffNum=(i)//data.lineCapacity
        print(staffNum)
        data.notes[i].drawNote(canvas,data,(data.dx*(i%data.lineCapacity)+data.margin+data.noteR),staffNum,data.notes[i].line)
        #data.dx+=10
    for i in range((staffNum+1)*2):
        data.staffs.append(Staff(i))
        data.staffs[i].drawStaff(canvas,data)

def run(width=300, height=300):
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
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
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

run(520, 800)