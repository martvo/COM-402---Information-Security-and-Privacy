import wave
import re

file = wave.open("martin.vold@epfl.ch.wav", mode="rb")

print(file.getparams())

nframes = file.getnframes()

file.rewind()
# The bytearray contains elements of 8 bits, that means that two and two elements makes up 
# a 16 bits where the lsb is at position 7 (from 0 to 15)
frame_bytes = bytearray(list(file.readframes(nframes)))

# As the lsb of 16 bit is at position 7, take every other element and get the lsb from it
lsb = [frame_bytes[i] & 1 for i in range(0, len(frame_bytes), 2)]


regex = re.compile("(COM402{).*(})")

# Create a string from the lsb we have, first every 8 bits (1 byte) to str, and join all of them to creat the string
string = "".join(chr(int("".join(map(str, lsb[i: i+8])), 2)) for i in range(0, len(lsb), 8))

# Search the string with the regex
token = regex.search(string).group()

print(token)