import wave
import struct
import sys


#import timeDomain

def almostEqual(x, y, epsilon = 10**-5):
    return abs(x-y) < epsilon

def wav_to_floats(wave_file): 
    #from https://stackoverflow.com/questions/7769981/how-to-convert-wave-file-to-float-amplitude
    #modified by Tara Stentz
    w = wave.open(wave_file)
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

# read the wav file specified as first command line arg
signal = wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/starryNight.wav")
#for i in range(0, (10)):
    #print(signal[i])
framerate=signal[1]
channels=signal[2]
#print(signal[0])
print(framerate,channels,len(signal[0]))

sampleFreqs=[]

window=[]
for i in range(len(signal[0])):
    window.append(signal[0][i])

#frequencies=DFT2(window)

def downSample(signal):
    #account for sampling rates other than 44k
    return signal[::24]

window2=downSample(window)
#print("window=",window2)

# print(len(window))
print(len(window2))


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
    for i in range(len(freqMagnitudes)//4):
        if almostEqual(freqMagnitudes[i][0],maxAmplitude):
            pass
        elif freqMagnitudes[i][0]>maxAmplitude:
            maxIndex=i
            maxAmplitude=freqMagnitudes[i][0]

    highFreq=convertToHz(maxIndex,framerate,len(window))
    print("max freq in Hz is", highFreq)

    return highFreq
    #return freqMagnitudes













def convertToHz(maxFreqIndex, framerate,winlen,): 
    print(maxFreqIndex,framerate,winlen)
    return (framerate*maxFreqIndex)/(winlen//channels)/24#(maxFreqIndex)*framerate/winlen


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







# window=[]
# for i in range(len(signal[0])//100):
#     window.append(signal[0][i])
# print(window)


def signalFrequencies(signal):
    #print("printing signal frequencies")
    sampleFreqs=[]
    sampWindow=256
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
        sampleFreqs.append(DFT2(window))
    return sampleFreqs


####MAKE IT SO YOU SHIFT GENTLY NOT RECTANGULARLY
testFrequencies=(signalFrequencies(window2))






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
print("fft over")


#################################################
# testAll and main
#################################################

def testAll():
    #   write test functions
    pass

def main():
    class Struct(object): pass
    dft = Struct()
    signal = wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/starryNight.wav")
    dft.framerate=signal[1]
    dft.channels=signal[2]

if __name__ == '__main__':
    main()
