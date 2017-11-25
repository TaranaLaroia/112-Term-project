import wave
import struct
import sys

def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short 
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    ###PUT ABOVE LINE BACK
    return a

# read the wav file specified as first command line arg
signal = wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/testPyAudio.wav")
#for i in range(0, (10)):
    #print(signal[i])

print ("read "+str(len(signal))+" frames")
print  ("in the range "+str(min(signal))+" to "+str(max(signal)))

import numpy as np
j = np.complex(0,1)
print("j is", j)

window=signal[:16]

import math
def DFT(window): #window is a list of samples being transformed
    samples=[]
    magnitudes=[]
    omega=2*math.pi/len(window)
    for i in range(len(window)):
        complexSample=(math.e**(-j*omega*i))*window[i]
        samples.append(complexSample)
        #print(samples[0])
        #print(complexSample,np.absolute(complexSample),np.real(complexSample),np.imag(complexSample))
        real=np.real(complexSample)
        imag=np.imag(complexSample)
        magnitudes.append(np.absolute(complexSample))
        #agnitudes.append("potato")
        #####GET MAGNITUDES OF SAMPLES
    #print(samples)
    return (magnitudes)

import statistics
def lowPassFilter(signal):
    newSignal=[]
    while len(signal)>=2:
        newSignal.append(statistics.mean(signal[0]+signal[1]))
        signal=signal[2:]
        print(mean(signal[0]+signal[1]))
    return newSignal

#signal=lowPassFilter(signal)  
###FIX LOW PASS FILTER CODE

#print(signal)  

def downSample(signal):
    return signal[::4]


print(DFT(signal))


# events-example0.py
# Barebones timer, mouse, and keyboard events

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate

    pass

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(-10,-10,data.width+10,data.height+10,fill="#222222")
    dx=0
    for i in range(0, (500)):
        color="lightskyblue"
        if i%2==1:
            color="indianred"
        canvas.create_line(dx,data.height//2,dx,data.height//2+signal[i]*30000,width=1,fill=color)
        dx+=1


####################################
# use the run function as-is
####################################

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
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(evenbt, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#run(500, 800)