import numpy as np
from Audio import Audio
from Crypto.Random import get_random_bytes
import rsa
import struct
from BBS import BBS


class Cryptographer:
    def __init__(self, audio: Audio = None, stride=1, algorithm=None, key=None):
        if key is not None:
            self.alg = BBS(key=key.split(' ')[1:])
            self.msglen = int(key.split(' ')[0])
        else:
            self.alg = algorithm
        #print(self.alg)
        self.stride = stride
        self.audio = audio
        self.frame_size = len(audio.frame) - (len(audio.frame) % self.stride)
        self.frame, self.tail = audio.frame[:self.frame_size], \
                                audio.frame[self.frame_size:]
        self.frame = np.reshape(self.frame, (self.stride, int(len(self.frame) / self.stride)))

    def encrypt(self, text, filename):
        n_symbols = len(text)
        for i in range(n_symbols):
            self.encrypt_symbol(text[i])

        self.frame = np.reshape(self.frame, (1, self.frame_size))[0]
        if not len(self.tail) == 0:
            self.frame = list(self.frame) + list(self.tail)
        self.frame = np.array(self.frame, dtype=np.int16)
        self.write_frame(filename)

    def encrypt_symbol(self, symbol):
        answer = ''
        symbol_stream = hex(symbol.encode('utf-8')[0])[2:]
        for i in symbol_stream:
            indx = self.alg.getdigit(n_bytes=4) % self.frame_size
            label = indx % self.stride
            column = type(indx)(indx / self.stride)
            self.frame[label][column] = np.int16(self.frame[label][column] & 0xfff0) + np.int16(
                int('0x000{}'.format(i), base=16))
            answer += hex(int(self.frame[label][column] & 0x000f))[2:]

    def write_frame(self, name):
        self.audio.write_to_file(self.frame, name=name)

    def decode(self):
        n_symbols = self.msglen
        string = ''
        for i in range(n_symbols):
            string += self.read_symbol()
        result = bytes.fromhex(string).decode('utf-8')
        return result

    def read_symbol(self):
        sym = ""
        for i in range(2):
            indx = self.alg.getdigit(n_bytes=4) % self.frame_size
            label = indx % self.stride
            column = type(indx)(indx / self.stride)
            sym += hex(int(self.frame[label][column] & 0x000f))[2:]
        return sym

    def __str__(self):
        return """
len frame = {}
len tail = {}
stride = {}""".format(self.frame.shape, len(self.tail), self.stride)
