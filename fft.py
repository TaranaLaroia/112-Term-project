import wave
import struct
import sys

#import timeDomain

def almostEqual(x, y, epsilon = 10**-5):
    return abs(x-y) < epsilon

def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short 
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    #a = [float(val) / pow(2, 15) for val in a]
    ###PUT ABOVE LINE BACK
    
    return (a,w.getframerate())

# read the wav file specified as first command line arg
signal = wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/pianoG.wav")
#for i in range(0, (10)):
    #print(signal[i])
framerate=signal[1]

window=[]
for i in range(256):
    window.append(signal[0][i])







def dcOffset(signal):
    sum=0
    for i in range(len(signal)):
        sum+=(signal[i])
    return sum/len(signal)

def removeDCOffset(signal,dcOffset):
    for i in range(len(signal)):
        signal[i]-=dcOffset
    return signal









print ("read "+str(len(signal))+" frames")
print  ("in the range "+str(min(signal[0]))+" to "+str(max(signal[0])))

import numpy as np
j = np.complex(0,1)

#window=signal[0][4000:5024]
#print(window)

import math
def DFT(window): #window is a list of samples being transformed
    samples=[]
    magnitudes=[]
    omega=framerate/len(window) #signal[1]=framerate
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


def DFT2(window):

    dco=dcOffset(window)
    window=removeDCOffset(window,dco)



    omega=math.pi*2/len(window)
    frequencies=[]
    freqMagnitudes=[]
    sum=0

    for k in range(len(window)):

        for n in range(len(window)):
            complexSample=window[n]*(math.e**(-j*omega*n*k))
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
    for i in range(len(freqMagnitudes)//2):
        if almostEqual(freqMagnitudes[i][0],maxAmplitude):
            pass
        elif freqMagnitudes[i][0]>maxAmplitude:
            maxIndex=i
            maxAmplitude=freqMagnitudes[i][0]

    highFreq=convertToHz(maxIndex,framerate,len(window))
    print("max freq in Hz is", highFreq)

    return freqMagnitudes


def convertToHz(maxFreqIndex, framerate,winlen,): 
    print(maxFreqIndex,framerate,winlen)
    return (framerate*maxFreqIndex)/winlen#(maxFreqIndex)*framerate/winlen


#frequencies=DFT2(window)
#print(frequencies)









def raisedCosWindow():
    window=[]
    for i in range(256):
        window.append(1-math.cos(i%(2*math.pi)))
    return window

#print(raisedCosWindow())




#print(DFT(window))
#print(DFT(signal))

#recursive fast implementation of dft
def FFT(signal): #signal is power of 2
   if len(signal)<=2:
   	   return DFT(signal)
   else:
   	#don't actually add idk how to combine them though
   	evens=signal[::2]
   	odds=signal[1::2]
   	return FFT(evens)+FFT(odds)

#print(FFT(window))
print("fft over")
