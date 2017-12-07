import wave
import struct
import sys
import numpy as np
import math
import copy
from note import *
import statistics


#taken from course notes
def almostEqual(x, y, epsilon = 10**-1):
    return abs(x-y) < epsilon


def wav_to_floats(wave_file,dft): 
    #from https://stackoverflow.com/questions/7769981/
    #how-to-convert-wave-file-to-float-amplitude
    #modified by Tara Stentz
    w = wave.open(wave_file)
    #get data of audio file in time domain
    try:
        astr = w.readframes(w.getnframes())
        # convert binary chunks to short 
        a = struct.unpack("%ih" % (w.getnframes()*w.getnchannels()), astr)    
        return (a,w.getframerate(),w.getnchannels())
    except:
        #if file corrupt, don't run code
        print("corrupt wav file :(")
        dft.corrupt=True




def makeWindow(signal):
    #get amplitudes of audio file in time domain from signal data
    window=[]
    for i in range(len(signal[0])):
        window.append(signal[0][i])
    return window





def downSample(signal,dft):
    #downsize size of file to speed up program
    return signal[::dft.downSamp]





def downSampCoef(dft):
    #find highest possible increment to downsample with
    highFreq=830.609 # G5#, highest frequency detectable
    nyquist=highFreq*2
    window=nyquist+nyquist//2 #extra space beyond nyquist threshold
    coef=1
    while coef*window<=dft.framerate:
        coef+=1
    return coef



def dcOffset(signal):
    #dc part of signal is average amplitude of whole signal
    sum=0
    for i in range(len(signal)):
        sum+=(signal[i])
    return sum/len(signal)

def removeDCOffset(signal,dcOffset):
    #remove dc part of signal, 0th frequency doesnt actually make noise
    for i in range(len(signal)):
        signal[i]-=dcOffset
    return signal




#########################################################
# The Fourier Transform Algorithm
#########################################################
#
# First: generate a set of monsters with varying attack levels
#   - number of monsters should be determined by field size
#   - level should be determined by hero level at beginning: half should be at
#     hero level, 1/4 one level above, 1/4 two levels above, and 1 five levels above
#   - distinguish monsters based on fill color?
#
# Second: determine where monsters should be placed on the field
#   - use random library to randomly place them
#   - but weight the placement so that easier monsters mostly appear closer to the hero
#   - non-randomly place the boss monster at the end
#
# Third: don't start monster movement until the gameplay starts
#   - have a class method to pause/unpause all monsters? or put a block in timerFired?


# The Fourier Transform takes a signal in the time domain and returns its components in the frequency domain

# 1. Remove dc offset from signal so it doesn’t interfere with frequency components
# 2. Signal will have ands many frequency components as there were time components, in this case heavily downsampled
# 3. For each frequency component, loop through entire signal
# 4. Use complex analysis with euler's equation to find frequency content in each time sample
# 5. After Fourier Transform, take largest frequency component of signal (harmonics will be filtered later)
# 6. Convert frequency component to Hz, mapping it from the sampling index to the sampling rate




#########################################################




def DFT2(window,dft):

    dco=dcOffset(window)
    window=removeDCOffset(window,dco)

    omega=math.pi*2/len(window)
    frequencies=[]
    freqMagnitudes=[]
    sum=0
    amps=[]

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

    fundamentals=[]
    

    for i in range(len(freqMagnitudes)//2):
        fundamentals.append(freqMagnitudes[i][0])
        if almostEqual(freqMagnitudes[i][0],maxAmplitude):
            pass
        elif freqMagnitudes[i][0]>maxAmplitude:
            maxIndex=i
            maxAmplitude=freqMagnitudes[i][0]

    newFundamentals=copy.copy(fundamentals)
    #print(fundamentals)
    newFundamentals.remove(maxAmplitude)
    print(max(newFundamentals))
    print(maxAmplitude,maxAmplitude/2)
    if maxAmplitude/2>statistics.mean(fundamentals)*100:# and almostEqual(max(newFundamentals),maxAmplitude/2):
        print("harmonic")
        maxAmplitude=maxAmplitude/2
        #maxIndex/=2






        #amps.append(maxAmplitude)

    #print("amps",amps)



    # if not almostEqual(maxAmplitude/2,0):
    #     print("harmonic")
    #     maxAmplitude=maxAmplitude/2
    #     maxIndex/=2





    # avg=0
    # for i in range(1,len(freqMagnitudes)//2):
    #     avg+=freqMagnitudes[i][0]

    #     avgSoFar=avg/i
    #     #print("avg so far",avgSoFar,i,len(freqMagnitudes)//4)
    #     weight=convertToHz(i,dft.framerate,len(window),dft)
    #     print(5+(weight/100))
    #     if freqMagnitudes[i][0]>(5+(weight/150))*avgSoFar:
    #         maxIndex=i-1
    #         fundamental=freqMagnitudes[i-1][0]
    #         print("fundamental.....................................",fundamental)
    #         break



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












#concise
def convertToHz(maxFreqIndex,framerate,winlen,dft): 
    return (dft.framerate*maxFreqIndex)/(winlen//dft.channels)/dft.downSamp#(maxFreqIndex)*framerate/winlen


# frequencies=DFT2(window2[:512])
# print(frequencies)






def beatDetection(frequencies,dft):
    beatLength=[1 for i in range(len(frequencies))]
    sampWindow=dft.sampleWindow
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
    for i in range(len(beatLength)-1):
        if beatLength[i]==2 and beatLength[i+1]!=2and beatLength[i-1]!=2:
            halfNotes.append(i)
        elif beatLength[i]==2 and beatLength[i+1]==2 and beatLength[i+2]==2:
            wholeNotes.append(i)
    dft.halfNotes=halfNotes
    dft.wholeNotes=wholeNotes
    print(halfNotes)
    print(wholeNotes)



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
    highKey=831 #G5#, highest key in detectable range
    # while newFrequencies[0]<lowKey:
    #     newFrequencies=newFrequencies[1:]

    for frequency in frequencies:
        if frequency>=lowKey:
            newFrequencies.append(frequency)


    return newFrequencies


def filterHarmonics(frequencies,dft):
    # filteredFreqs=[]
    # for i in range(1,len(frequencies)):
    #     if almostEqual(frequencies[i],frequencies[i-1]*2,10):
    #         filteredFreqs.append(frequencies[i]/2)
    #         print(1/0)
    #     else:
    #         #print("fixed",frequencies[i])
    #         filteredFreqs.append(frequencies[i])
    print(frequencies)
    print("filtering",len(frequencies))
    sampWindow=dft.sampleWindow

    for i in range(1,len(frequencies)):
        print(i)
        if almostEqual(frequencies[i],frequencies[i-1]*2):
            print("step one")
            #print(1/0)
            if statistics.mean(dft.window[(i-1)*sampWindow:(i)*sampWindow])>=statistics.mean(dft.window[(i-2)*sampWindow:(i-1)*sampWindow]):
                print("step two")
                #print(2/0)
                frequencies[i]/=2

    print(frequencies)




    return frequencies


def filterOutliers(frequencies):
    newFrequencies=[]#copy.copy(frequencies)
    highKey=831 #G5#, highest key in detectable range
    # while newFrequencies[0]<lowKey:
    #     newFrequencies=newFrequencies[1:]

    for frequency in frequencies:
        if frequency<=highKey:
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
        note.findKey(dft)
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
