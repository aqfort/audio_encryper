import argparse
from Audio import Audio
import rsa
from Cryptographer import Cryptographer
from BBS import BBS

parser = argparse.ArgumentParser(description='Encryptor parser')
parser.add_argument('-i', type=str, default=r'/home/bvdvlg/PycharmProjects/untitled/mozart_before.wav')
parser.add_argument('-o', type=str, default=r'/home/bvdvlg/PycharmProjects/untitled/mozart_after.wav')

with open("/home/bvdvlg/public_key.txt", "r") as pr:
    private_str = pr.read().split(" ")
    public = rsa.PublicKey(int(private_str[0]), int(private_str[1]))

args = parser.parse_args()
audio = Audio(filename=args.i)
encrypter = Cryptographer(audio=audio, algorithm=BBS())
encrypter.encrypt("World goo!"*1000, filename=args.o, publicKey=public)
print("Successfully encrypted")
