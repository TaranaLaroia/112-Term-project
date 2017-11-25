import pyaudio
import wave
from array import array
from struct import pack

#modified code from audio semi-optional lecture slides
def run(file):
    CHUNK = 1024 #measured in bytes

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    print(wf.getnchannels())
    print(wf.getframerate())
    print(p.get_format_from_width(wf.getsampwidth()))
    print(wf.readframes(1))

    print(int.from_bytes(wf.readframes(10), byteorder='little', signed=False))
    #print(bytes.fromhex(wf.readframes(800)))

    print(bytes_to_int(wf.readframes(10)))

    sampfreq=2


    p.terminate()


def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 1024 + int(b)

    return result



run("/Users/taranalaroia/Documents/TERMPROJECT/440sin3.wav")



import wave
import struct
import sys

def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short 
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a

# read the wav file specified as first command line arg
signal = wav_to_floats("/Users/taranalaroia/Documents/TERMPROJECT/testPyAudio.wav")
for i in range(0, 1000):
    print(signal[i])
print ("read "+str(len(signal))+" frames")
print  ("in the range "+str(min(signal))+" to "+str(max(signal)))

