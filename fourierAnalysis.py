# fourier transform file, where all sound analysis is done
# gets passed in audio signal, manipulates to get notes for sheet music

# contains wav_to_floats, which time samples audio, dft, which retrieves
# frequency content, signalFrequencies, which gets frequencies of entire
# signal, as well as many other signal filters that will map frequencies
# to notes to write sheet music

import wave
import struct
import sys
import numpy as np
import math
import copy
import statistics
from note import *


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


def downSampCoef(framerate):
    #find highest possible increment to downsample with
    highFreq=830.609 # G5#, highest frequency detectable
    nyquist=highFreq*2
    window=nyquist+nyquist//2 #extra space beyond nyquist threshold
    coef=1
    while coef*window<=framerate:
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

# The Fourier Transform takes a signal in the time domain
# and returns its components in the frequency domain

# 1. Remove dc offset from signal so it doesn’t interfere
# with frequency components
# 2. Signal will have ands many frequency components as there
# were time components, in this case heavily downsampled
# 3. For each frequency component, loop through entire signal
# 4. Use complex analysis with euler's equation to find
# frequency content in each time sample
# 5. After Fourier Transform, take largest frequency component
# of signal (harmonics will be filtered later)
# 6. Convert frequency component to Hz, mapping it from the
# sampling index to the sampling rate


#########################################################


# makes extensive use of Signals and Systems by Alan Oppenheim
# see credits for more details

def DFT(window,dft):

    #remove dc content from signal
    dco=dcOffset(window)
    window=removeDCOffset(window,dco)

    omega=math.pi*2/len(window)
    freqMagnitudes=[]
    sum=0

    for k in range(len(window)):
        for n in range(len(window)):
            complexSample=window[n]*(math.e**(-dft.j*omega*n*k))
            #euler's equation adapted into signal processing
            sum+=complexSample

        magnitude=np.absolute(sum)
        if not almostEqual(0,magnitude):
            freqMagnitudes.append((magnitude,k))
        else: 
            freqMagnitudes.append((0,k)) 
        sum=0

    maxIndex=0
    maxAmplitude=0

    #//2 for nyquist filtering, //2 again for low pass windowing
    for i in range(len(freqMagnitudes)//4):
        #find largest frequency component
        if almostEqual(freqMagnitudes[i][0],maxAmplitude):
            pass
        elif freqMagnitudes[i][0]>maxAmplitude:
            maxIndex=i
            maxAmplitude=freqMagnitudes[i][0]

    #convert index to Hz
    highFreq=convertToHz(maxIndex,dft.framerate,len(window),dft)

    return highFreq



def convertToHz(maxFreqIndex,framerate,winlen,dft): 
    #map frequencies from index to Hz
    df=(winlen//dft.channels)
    return (dft.framerate*maxFreqIndex)/df/dft.downSamp


def signalFrequencies(signal,dft):
    #break entire time signal into small chunks
    #run fourier transform on all of them
    sampleFreqs=[]
    sampWindow=dft.sampleWindow
    for i in range(len(signal)//sampWindow):
        window=[]
        for j in range(i*sampWindow,(i+1)*sampWindow):
            if j<len(signal):
                window.append(signal[j])
            else:
                window.append(0)
        sampleFreqs.append(DFT(window,dft))
    return sampleFreqs


def beatDetection(frequencies,dft):
    #detect length of notes
    beatLength=[1 for i in range(len(frequencies))]
    sampWindow=dft.sampleWindow
    for i in range(len(frequencies)-1):
        if almostEqual(frequencies[i],frequencies[i+1]):
            #if two frequencies are the same and amplitudes--, same note
            if statistics.mean(dft.window[i*sampWindow:(i+1)*sampWindow])\
            >=statistics.mean(dft.window[(i+1)*sampWindow:(i+2)*sampWindow]):
                beatLength[i]+=1
            #else same note played two different times
    return beatLength


def noteLengths(beatLength,dft):
    #take output from beat length and find half and whole notes
    halfNotes=[]
    wholeNotes=[]
    for i in range(len(beatLength)-1):
        if beatLength[i]==2 and beatLength[i+1]!=2and beatLength[i-1]!=2:
            halfNotes.append(i)
        elif beatLength[i]==2 and beatLength[i+1]==2 and beatLength[i+2]==2:
            wholeNotes.append(i)
    dft.halfNotes=halfNotes
    dft.wholeNotes=wholeNotes



def removeDeadSpace(frequencies):
    #gets rid of all frequencies<than min detectable frequency
    newFrequencies=[]
    lowKey=110 #A3, lowest key in detectable range

    for frequency in frequencies:
        if frequency>=lowKey:
            newFrequencies.append(frequency)

    return newFrequencies


def filterHarmonics(frequencies,dft):
    #remove extra harmonics from note that plays too long
    sampWindow=dft.sampleWindow

    for i in range(1,len(frequencies)):
        if almostEqual(frequencies[i],frequencies[i-1]*2):
            #if a frequency is 2x the one that came before it but
            #new note wasnt played it jumped to harmonic
            if statistics.mean(dft.window[(i-1)*sampWindow:(i)*sampWindow])\
            >=statistics.mean(dft.window[(i-2)*sampWindow:(i-1)*sampWindow]):
                frequencies[i]/=2

    return frequencies



def filterOutliers(frequencies):
    #remove all frequencies higher than detecable range
    newFrequencies=[]
    highKey=831 #G5#, highest key in detectable range

    for frequency in frequencies:
        if frequency<=highKey:
            newFrequencies.append(frequency)

    return newFrequencies


def getTempo(frequencies,dft):
    #use first note of song to set tempo
    #all other notes defined relative to first(quarter)
    tempo=1

    notes=getNotes(frequencies,dft)

    for i in range(1,len(notes)):
        if notes[i].key[0]==notes[i-1].key[0] and \
        notes[i].key != notes[i-1].key:
            notes[i].key = notes[i-1].key
            frequencies[i]/=2

    for i in range(len(notes)-1):
        if notes[i].key==notes[i+1].key:
            tempo+=1
        else:
            break

    return tempo


def getNotes(frequencies,dft):
    #map frequencies to notes
    notes=[]
    for frequency in frequencies:
        note=Note(frequency)
        notes.append(note)
        note.findKey(dft)
    return notes


def setTempo(testFrequencies,tempo):
    #increment list of all frequencies by changes
    return testFrequencies[::tempo]



def filterLengths(frequencies):
    if len(frequencies)<2:
        frequencies=[frequencies[0]]
    else: #extra harmonics from final notes
        frequencies=frequencies[:-2]
    return frequencies
