# 112-Term-project
THE PROJECT

What this program does is take in a monophonic piano input with notes in the range A2-G5#, and does several layers of signal processing and sound analysis to output the sheet music for the audio

When run, user is prompted to select a wav file to analyze, which the program will take time processing and eventually tkinter will draw the sheet music output

This project makes use of tkinter and numPy


Breakdown of all files:

main file is where the program is run

fourierAnalysis file contains the super math heavy algorithmically complex stuff, where all of the notes are manipulated

keys file contains two dictionaries that map frequencies to notes and notes to the staff lines they go on

drawMusic file draws sheet music

staff and note are classes that are used mostly for draw methods but some other properties too

tpTestCases are test functions for various assertion-testable things written (doesn't include graphic testing)


Test Files Included:
440HzSin
A4
G5
C3
A4#
F5
C5#
D5#
E5
D5
A-C-E
Fur Elise


CREDITS

This project would not have been possible without the help of

People:
Tara Stentz
Professor Tom Sullivan
Professor Noel Walkington
Professor Rick Carley
Professor Ryan Riley
Anne Silbaugh
Vasu Agrawal

Textbooks:
Signals and Systems Sixth Edition by Alan Oppenheim
Fundamentals of Electrical Engineering by Giorgio Rizzoni
Fundamentals of Physics Fifth Edition by David Halliday, Robert Resnick, and Jearl Walker
Teach Yourself Calculus by P. Abbot

Websites:
https://www.onlineconverter.com/midi-to-wav
https://en.wikipedia.org/wiki/Piano_key_frequencies
https://freesound.org
http://www.wolframalpha.com
https://audio.online-convert.com/convert-to-wav
https://en.wikipedia.org/wiki/Finite_impulse_response
http://www.eas.uccs.edu/~mwickert/ece2610/lecture_notes/ece2610_chap5.pdf
https://en.wikipedia.org/wiki/Fast_Fourier_transform
http://freewavesamples.com
https://www.youtube.com/watch?v=EsJGuI7e_ZQ
https://www.youtube.com/watch?v=WvWuco54FHg
http://www.dspguide.com/ch12/2.htm
https://en.wikipedia.org/wiki/Cooley–Tukey_FFT_algorithm
https://en.wikipedia.org/wiki/Cepstrum
http://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
https://en.wikipedia.org/wiki/Discrete_Fourier_transform
https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/
http://www.thefouriertransform.com


Special thanks to tp mentor Rishabh Chatterjee
