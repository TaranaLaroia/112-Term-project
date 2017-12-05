import wave
import struct
import sys
import numpy as np
import math
import copy
from note import *
#import drawMusic

#taken from course notes
def almostEqual(x, y, epsilon = 10**-2):
    return abs(x-y) < epsilon

def wav_to_floats(wave_file,dft): 
    #from https://stackoverflow.com/questions/7769981/how-to-convert-wave-file-to-float-amplitude
    #modified by Tara Stentz
    w = wave.open(wave_file)
    try:
        astr = w.readframes(w.getnframes())
        print(type(astr))
        print("len=",len(astr))
        # convert binary chunks to short 
        #print(w.getnframes())
        print("framesxchannels",w.getnframes()*w.getnchannels())
        print(struct.calcsize("%ih" % (w.getnframes()*w.getnchannels())))
        a = struct.unpack("%ih" % (w.getnframes()*w.getnchannels()), astr)
    #a = [float(val) / pow(2, 15) for val in a]
    ###PUT ABOVE LINE BACK
    
        return (a,w.getframerate(),w.getnchannels())
    except:
        print("corrupt wav file :(")
        dft.corrupt=True

# read the wav file specified as first command line arg
#print(signal[0])


def makeWindow(signal):
    window=[]
    for i in range(len(signal[0])):
        window.append(signal[0][i])
    return window





#frequencies=DFT2(window)

def downSample(signal,dft):
    #account for sampling rates other than 44k
    return signal[::dft.downSamp]

#print("window=",window2)

# print(len(window))


def downSampCoef(dft):
    highFreq=830.609 # G5#, highest frequency detectable
    nyquist=highFreq*2
    window=nyquist*3/2
    coef=1
    while coef*window<=dft.framerate:
        coef+=1
    return coef



def dcOffset(signal):
    sum=0
    for i in range(len(signal)):
        sum+=(signal[i])
    return sum/len(signal)

def removeDCOffset(signal,dcOffset):
    for i in range(len(signal)):
        signal[i]-=dcOffset
    return signal






# print ("read "+str(len(signal))+" frames")
# print  ("in the range "+str(min(signal[0]))+" to "+str(max(signal[0])))


#window=signal[0][4000:5024]
#print(window)

import math
def DFT(window): #window is a list of samples being transformed
    samples=[]
    magnitudes=[]
    omega=dft.framerate/len(window) #signal[1]=framerate
    max=(0,0)
    sum=0
    x=[]

    for i in range(len(window)):
        complexSample=window[i]*(math.e**(-j*omega*i))
        sum+=complexSample
        #samples.append(complexSample)
        samples.append(sum)
        #print(samples[0])
        #print(complexSample,np.absolute(complexSample),np.real(complexSample),np.imag(complexSample))
        real=np.real(complexSample)
        imag=np.imag(complexSample)
        magnitude=np.absolute(sum)
        if magnitude>=max[0]:
            max=(magnitude,window[i],i*omega)
            #print("overwrite")
        # if abs(magnitude)>0.1:
        magnitudes.append(magnitude)
        #agnitudes.append("potato")
        #####GET MAGNITUDES OF SAMPLES
    #print(samples)
    return (magnitudes)

#DC=[1 for i in range(500)]
#print (DC)




def DFT2(window,dft):

    dco=dcOffset(window)
    window=removeDCOffset(window,dco)

    omega=math.pi*2/len(window)
    frequencies=[]
    freqMagnitudes=[]
    sum=0

    for k in range(len(window)):

        for n in range(len(window)):
            complexSample=window[n]*(math.e**(-dft.j*omega*n*k))
            #complexSample=window[k]*(math.cos(omega*k*n)-j*math.sin(omega*k*n))
            #print(complexSample)
            sum+=complexSample

        frequencies.append(sum)
        magnitude=np.absolute(sum)
        if not almostEqual(0,magnitude):
            freqMagnitudes.append((magnitude,k))
        else: 
            freqMagnitudes.append((.01,k))
        sum=0
    #print(freqMagnitudes)

    maxIndex=0
    maxAmplitude=0
    fundamental=0
    maxAmpIndex=0

    # for i in range(len(freqMagnitudes)//4):
    #     if almostEqual(freqMagnitudes[i][0],maxAmplitude):
    #         pass
    #     elif freqMagnitudes[i][0]>maxAmplitude:
    #         maxIndex=i
    #         maxAmplitude=freqMagnitudes[i][0]




    avg=0
    for i in range(1,len(freqMagnitudes)//2):
        avg+=freqMagnitudes[i][0]

        avgSoFar=avg/i
        #print("avg so far",avgSoFar,i,len(freqMagnitudes)//4)
        weight=convertToHz(i,dft.framerate,len(window),dft)
        print(5+(weight/90))
        if freqMagnitudes[i][0]>(5+(weight/90))*avgSoFar:
            maxIndex=i-1
            fundamental=freqMagnitudes[i-1][0]
            print("fundamental.....................................",fundamental)
            break



    #     if freqMagnitudes[i][0]>maxAmplitude:
    #         maxAmpIndex=i
    #         maxAmplitude=freqMagnitudes[i][0]
    # if fundamental==0:
    #     fundamental=maxAmplitude
    #     maxIndex=maxAmpIndex
    #     print("max......................",fundamental)




    highFreq=convertToHz(maxIndex,dft.framerate,len(window),dft)
    print("max freq in Hz is", highFreq)

    return highFreq
    #return freqMagnitudes













def convertToHz(maxFreqIndex,framerate,winlen,dft): 
    #print(maxFreqIndex,dft.framerate,winlen)
    return (dft.framerate*maxFreqIndex)/(winlen//dft.channels)/dft.downSamp#(maxFreqIndex)*framerate/winlen


# frequencies=DFT2(window2[:512])
# print(frequencies)






def removeNoise(signal):
    #get rid of dead space before signal
    sampWindow=256
    newSignal=signal
    reverse=signal[::-1]
    for i in range (len(signal)//sampWindow):
        if almostEqual(DFT2(signal[sampWindow*i:sampWindow*(i+1)]),0):
            print("zeroes in front")
            newSignal=newSignal[sampWindow:]
        else:
            print("no more front zeroes")
            break
    # for i in range (len(signal)//sampWindow):
    #     if almostEqual(DFT2(reverse[sampWindow*i:sampWindow*(i+1)]),0):
    #         newSignal=newSignal[:sampWindow]
    #         print("zeroes in back")
    #     else:
    #         print("no more back zeroes")
    #         break
    return newSignal


# print(window)
# window=removeNoise(window)
# print(window)




def beatDetection(frequencies,dft):
    beatLength=[1 for i in range(len(frequencies))]
    sampWindow=256
    for i in range(len(frequencies)-1):
        if almostEqual(frequencies[i],frequencies[i+1]):
            if statistics.mean(dft.window[i*sampWindow:(i+1)*sampWindow])>=statistics.mean(dft.window[(i+1)*sampWindow:(i+2)*sampWindow]):
                beatLength[i]+=1
                #beatLength[i+1]+=1
    return beatLength





def noteLengths(beatLength,dft):
    halfNote=2
    wholeNote=3 #2^3=8
    halfNotes=[]
    wholeNotes=[]
    for i in range(len(beatLength)):
        if beatLength[i]==2 and beatLength[i-1]!=2:
            halfNotes.append(i)
        elif beatLength[i]==2 and beatLength[i-1]==2:
            wholeNotes.append(i-1)
            halfNotes.pop()
    dft.halfNotes=halfNotes
    dft.wholeNotes=wholeNotes
    print(halfNotes)
    print(wholeNotes)




# window=[]
# for i in range(len(signal[0])//100):
#     window.append(signal[0][i])
# print(window)


def signalFrequencies(signal,dft):
    #print("printing signal frequencies")
    sampleFreqs=[]
    sampWindow=dft.sampleWindow
    for i in range(len(signal)//sampWindow):
        window=[]
        #print("i=",i)
        for j in range(i*sampWindow,(i+1)*sampWindow):
            #print("j=",j)
            if j<len(signal):
                window.append(signal[j])
            else:
                window.append(0)
        #print(window)
        sampleFreqs.append(DFT2(window,dft))
    return sampleFreqs


####MAKE IT SO YOU SHIFT GENTLY NOT RECTANGULARLY




def removeDeadSpace(frequencies): #THE ONE THAT WORKS NEEDS TESTING THOUGH
    newFrequencies=[]#copy.copy(frequencies)
    lowKey=110 #A3, lowest key in detectable range

    # while newFrequencies[0]<lowKey:
    #     newFrequencies=newFrequencies[1:]

    for frequency in frequencies:
        if frequency>=lowKey:
            newFrequencies.append(frequency)


    return newFrequencies








def getTempo(frequencies):
    # beatCopy=copy.copy(beatLength)
    tempo=1
    # while beatCopy[1]!=1:
    #   pace+=1
    #   beatCopy=beatCopy[1:]

    notes=getNotes(frequencies)

    for i in range(len(notes)-1):
        if notes[i].key==notes[i+1].key:
            tempo+=1
        else:
            break

    return tempo




def getNotes(frequencies):
    notes=[]
    for frequency in frequencies:
        note=Note(frequency)
        notes.append(note)
        note.findKey()
        #print(note)
    return notes






def setTempo(testFrequencies,tempo):
    return testFrequencies[::tempo]










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




def raisedCosWindow():
    window=[]
    for i in range(256):
        window.append(1-math.cos(i%(2*math.pi)))
    return window

#print(raisedCosWindow())

def separate(signal):
    evens=signal[::2]
    odds=signal[1::2]
    return (evens+odds)



#print(DFT(window))
#print(DFT(signal))

#recursive fast implementation of dft
def FFT(signal): #signal is power of 2
   if len(signal)<2:
   	   return (signal)
   else:
   	#don't actually add idk how to combine them though
    signal=separate(signal)
    evens=DFT2(signal[:len(signal)//2])
    odds=DFT2(signal[len(signal)//2:])

    newSignal=[0]*len(signal)

    for i in range(len(signal)//2):
        even=signal(i)
        odd=signal(i+len(signal)//2)
        omega=math.pi*2/len(signal)
        w=(math.e**(-j*omega*k))

        newSignal[i]=even+w*odd
        newSignal[i+len(signal)//2]=even-w*odd


    return FFT(newSignal)

#print(FFT(window))


#################################################
# testAll and main
#################################################

def testAll():
    # dear Tarana please remember to write test functions
    pass



print("fft over")
