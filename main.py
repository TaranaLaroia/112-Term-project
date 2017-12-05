from fft import *
import drawMusic

def main():
    class Struct(object): pass
    dft = Struct()
    dft.corrupt=False
    signal=wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/grandPiano.wav",dft)
    if not dft.corrupt:
        dft.framerate=signal[1]
        dft.downSamp=downSampCoef(dft)
        print("downSamp",dft.downSamp)
        dft.channels=signal[2]
        dft.window=makeWindow(signal)
        dft.window=downSample(dft.window,dft)
        dft.j = np.complex(0,1)
        dft.sampleWindow=256
        dft.frequencies=(signalFrequencies(dft.window,dft))
        print(dft.frequencies)
        dft.frequencies=removeDeadSpace(dft.frequencies)
        dft.tempo=getTempo(dft.frequencies)
        dft.frequencies=setTempo(dft.frequencies,dft.tempo)
        dft.beatLength=beatDetection(dft.frequencies,dft)
        noteLengths(dft.beatLength,dft)
        print(dft.beatLength,dft.halfNotes,dft.wholeNotes)
        drawMusic.sheetMusic(dft, 1000, 800)
        

if __name__ == '__main__':
    main()