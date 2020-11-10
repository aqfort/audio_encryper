import argparse
from Audio import Audio
import rsa
from Cryptographer import Cryptographer
from BBS import BBS

parser = argparse.ArgumentParser(description='Encryptor parser')
parser.add_argument('-i', type=str, default=r'/home/bvdvlg/PycharmProjects/untitled/mozart_after.wav')

with open("/home/bvdvlg/private_key.txt", "r") as pr:
    private_str = pr.read().split(" ")
    private = rsa.PrivateKey(int(private_str[0]), int(private_str[1]), int(private_str[2]), int(private_str[3]), int(private_str[4]))

args = parser.parse_args()
audio = Audio(filename=args.i)
session_key = rsa.decrypt(bytes(audio.getkey(512)), private)
session_key = session_key.decode('utf-8')
decoder = Cryptographer(audio=audio, key=session_key)
res = decoder.decode()
print(res)