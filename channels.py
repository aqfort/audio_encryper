from Audio import Audio
from Cryptographer import Cryptographer
from BBS import BBS
import numpy as np
import rsa
from Crypto.Random import get_random_bytes

public, private = rsa.newkeys(512)
alg = BBS()
audio = Audio(filename=r'D:\mozart_before.wav')
crypter = Cryptographer(audio=audio, algorithm=alg)
crypter.encrypt("Hello world!"*100, filename=r'D:\mozart_new.wav', publicKey=public)
audio2 = Audio(filename=r'D:\mozart_new.wav')
session_key = rsa.decrypt(bytes(audio2.getkey(512)), private)
session_key = session_key.decode('utf-8')
crypter2 = Cryptographer(audio=audio2, key=session_key)
print(crypter2.decode())
