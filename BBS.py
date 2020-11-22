import rsa
from Crypto.Random import get_random_bytes
import numpy as np

utypes = dict({1: np.uint8, 2: np.uint16, 4: np.uint32, 8: np.uint64})
types = dict({1: np.int8, 2: np.int16, 4: np.int32, 8: np.int64})


class BBS:
    def __init__(self, x_0=None, p=None, q=None, key=None):
        if key is not None:
            self.__init__(x_0=int(key[0]), p=int(key[1]), q=int(key[2]))
            return
        if p is None or q is None or x_0 is None:
            self.p, self.q = self.check_find_pq(p, q)
            self.x_0 = self.check_find_x_0(x_0)
        else:
            self.p, self.q, self.x_0 = p, q, x_0
        self.M = self.p * self.q
        self.x_current = int(self.x_0)

    @staticmethod
    def check_find_pq(p, q):
        if p is None or q is None:
            p, q = rsa.key.find_p_q(32)
        return p, q

    def get_key(self):
        return str(self.x_0) + " " + str(self.p) + " " + str(self.q)

    @staticmethod
    def check_find_x_0(x_0):
        if x_0 is None:
            x_0 = np.frombuffer(get_random_bytes(4), np.uint16)[0]
        return x_0

    def __str__(self):
        return '''
Name: BBS
x_0 = {}
p = {}
q = {}
x_current = {}'''.format(self.x_0, self.p, self.q, self.x_current)

    def countn(self, n=1):
        sample = int(self.x_current ** 2 % self.M)
        result = [sample, ]
        for i in range(1, n):
            sample = (sample**2 % self.M)
            result.append(sample)
        self.x_current = sample
        return result

    def getdigit(self, n_bytes=4):
        lst = [str(bin(i).count('1') % 2) for i in self.countn(n_bytes * 8)]
        return np.uint32(int('0b' + ''.join(lst), base=2))

    def getndigits(self, n, size):
        return [self.getdigit(size) for i in range(n)]
