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

window=signal[:128]

import math
def DFT(window): #window is a list of samples being transformed
    samples=[]
    magnitudes=[]
    omega=2*math.pi/len(window)
    max=(0,0)
    for i in range(len(window)):
        complexSample=(math.e**(-j*omega*i))*window[i]
        samples.append(complexSample)
        #print(samples[0])
        #print(complexSample,np.absolute(complexSample),np.real(complexSample),np.imag(complexSample))
        real=np.real(complexSample)
        imag=np.imag(complexSample)
        magnitude=np.absolute(complexSample)
        if magnitude>=max[0]:
            max=(magnitude,window[i],i*omega)
            #print("overwrite")
        # if abs(magnitude)>0.1:
        #     magnitudes.append((magnitude,i))
        #agnitudes.append("potato")
        #####GET MAGNITUDES OF SAMPLES
    #print(samples)
    return (max)

print(DFT(window))
print(DFT(signal))

#recursive fast implementation of dft
def FFT(signal): #signal is power of 2
   if len(signal)<=2:
   	   return DFT(signal)
   else:
   	#don't actually add idk how to combine them though
   	evens=signal[::2]
   	odds=signal[1::2]
   	return FFT(evens)+FFT(odds)

print(FFT(window))

