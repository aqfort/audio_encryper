import numpy as np
from Audio import Audio
from Crypto.Random import get_random_bytes
import rsa
import struct
from BBS import BBS

opg = set()
wr_opg = set()
com_ind = []

class Cryptographer:
    def __init__(self, audio: Audio = None, stride=1, algorithm=None, key=None,  test=None):
        if key is not None:
            self.alg = BBS(key=key.split(' ')[1:])
            self.msglen = int(key.split(' ')[0])
        else:
            self.alg = algorithm
        if test is not None:
            self.enc = test.split(" ")
        self.stride = stride
        self.audio = audio
        self.frame_size = len(audio.frame) - (len(audio.frame) % self.stride)
        self.frame, self.tail = audio.frame[:self.frame_size], \
                                audio.frame[self.frame_size:]
        self.frame = np.reshape(self.frame, (self.stride, int(len(self.frame) / self.stride)))

    def encrypt(self, text, filename, publicKey : rsa.PublicKey):
        n_symbols = len(text)
        st = ""
        for i in range(n_symbols):
            st += self.encrypt_symbol(text[i]) + " "
        self.frame = np.reshape(self.frame, (1, self.frame_size))[0]
        if not len(self.tail) == 0:
            self.frame = list(self.frame) + list(self.tail)
        self.frame = np.array(self.frame, dtype=np.int16)
        sesskey = "{} {}".format(len(text), self.alg.get_key()).encode('utf-8')
        sesskey = rsa.encrypt(sesskey, pub_key=publicKey)
        self.frame[0:len(np.frombuffer(sesskey, dtype=np.int16))] = np.frombuffer(sesskey, dtype=np.int16)
        self.write_frame(filename)
        return st

    def encrypt_symbol(self, symbol):
        answer = ''
        symbol_stream = hex(symbol.encode('utf-8')[0])[2:]
        for i in symbol_stream:
            indx = self.alg.getdigit(n_bytes=4) % self.frame_size
            while indx in opg or indx < 1000:
                indx = self.alg.getdigit(n_bytes=4) % self.frame_size
            opg.add(indx)
            com_ind.append(indx)
            label = indx % self.stride
            column = type(indx)(indx / self.stride)
            self.frame[label][column] = np.int16(self.frame[label][column] & 0xfff0) | np.int16(int(i, base=16))
            answer += hex(int(self.frame[label][column] & 0x000f))[2:]
        return answer

    def write_frame(self, name):
        self.audio.write_to_file(self.frame, name=name)

    def decode(self):
        n_symbols = self.msglen
        string = ''
        for i in range(n_symbols):
            sym, indx = self.read_symbol()
            string += sym + " "
        result = bytes.fromhex(string).decode('utf-8')
        return result

    def read_symbol(self):
        sym = ""
        indxs = []
        for i in range(2):
            indx = self.alg.getdigit(n_bytes=4) % self.frame_size
            while indx in wr_opg or indx < 1000:
                indx = self.alg.getdigit(n_bytes=4) % self.frame_size
            wr_opg.add(indx)
            indxs.append(indx)
            label = indx % self.stride
            column = type(indx)(indx / self.stride)
            sym += hex(np.int16(self.frame[label][column] & 0x000f))[2:]
        return sym, indxs

    def __str__(self):
        return """
len frame = {}
len tail = {}
stride = {}""".format(self.frame.shape, len(self.tail), self.stride)

