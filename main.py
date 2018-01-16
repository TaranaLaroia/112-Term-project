# Main file that runs entire program
# contains mostly top-level code that calls other functions,
# including main, audioFile(which lets user select file), and
# getTitle(which takes path and extracts title from it)


from fourierAnalysis import *
import drawMusic

def analyzeAudio(dft,signal):
    dft.framerate=signal[1]
    dft.downSamp=downSampCoef(dft.framerate)
    dft.channels=signal[2]
    dft.window=makeWindow(signal)
    dft.window=downSample(dft.window,dft)
    dft.j=np.complex(0,1)
    dft.sampleWindow=256 #window where time samples go through dft
    dft.frequencies=(signalFrequencies(dft.window,dft))
    dft.frequencies=removeDeadSpace(dft.frequencies)
    dft.frequencies=filterHarmonics(dft.frequencies,dft)
    dft.frequencies=filterOutliers(dft.frequencies)
    if dft.frequencies[0]!=dft.frequencies[1]:
        dft.frequencies.pop(0) #remove extra dead space
    dft.tempo=getTempo(dft.frequencies,dft)
    dft.frequencies=setTempo(dft.frequencies,dft.tempo)
    dft.beatLength=beatDetection(dft.frequencies,dft)
    noteLengths(dft.beatLength,dft)
    dft.frequencies=filterLengths(dft.frequencies)

from tkinter import Tk
from tkinter.filedialog import askopenfilename
#taken from https://stackoverflow.com/questions/3579568/
#choosing-a-file-in-python-with-simple-dialog
def audioFile():
    Tk().withdraw()
    filename = askopenfilename()
    return (filename)


def getTitle(path):
    files=path.split("/")
    wav=4 #4 characters in ".wav"
    return (files[-1][:-wav])


def main():
    audio=audioFile()
    class Struct(object): pass
    dft = Struct()
    dft.corrupt=False
    dft.audio=None
    dft.title=getTitle(audio)
    signal=wav_to_floats(audio,dft)
    if not dft.corrupt:
        analyzeAudio(dft,signal)
        drawMusic.sheetMusic(dft, 600, 500)
        

if __name__ == '__main__':
    main()
