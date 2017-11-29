import wave
import struct
import sys
from fft import *

def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short 
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    #a = [float(val) / pow(2, 15) for val in a]
    ###PUT ABOVE LINE BACK
    
    return (a,w.getframerate())

# read the wav file specified as first command line arg
signal = wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/440sin3.wav")
#for i in range(0, (10)):
    #print(signal[i])
window=[]
for i in range(1024,2048):
    window.append(signal[0][i])

window2=[]

for i in range(len(window)):
	window2.append(window[i]-700000000)



framerate=signal[1]

def dcOffset(signal):
	sum=0
	for i in range(len(signal)):
		sum+=(signal[i])
	return sum/len(signal)

def removeDCOffset(signal,dcOffset):
	for i in range(len(signal)):
		signal[i]-=dcOffset
	return signal


#print(dcOffset(signal[0][1024:2048]))
print(dcOffset([8]*1000))

import math

sinWav=[]
for i in range(1024):
    sinWav.append(math.sin((2*math.pi/8)*i))

print(dcOffset(window2))


print(DFT2(window2))