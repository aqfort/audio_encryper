#!/usr/bin/env python3
import argparse
from Audio import Audio
import rsa
from Cryptographer import Cryptographer
from BBS import BBS

parser = argparse.ArgumentParser(description='Encryptor parser')
parser.add_argument('-i', type=str, default=r'mozart_before.wav')
parser.add_argument('-o', type=str, default=r'mozart_after.wav')
parser.add_argument('-msg', type=str, default="Hello world!")

with open("public_key.txt", "r") as pr:
    private_str = pr.read().split(" ")
    public = rsa.PublicKey(int(private_str[0]), int(private_str[1]))

args = parser.parse_args()
audio = Audio(filename=args.i)
encrypter = Cryptographer(audio=audio, algorithm=BBS())
encrypter.encrypt(args.msg, filename=args.o, publicKey=public)
print("Successfully encrypted")
