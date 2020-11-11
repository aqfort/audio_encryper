#!/usr/bin/env python3
import argparse
from Audio import Audio
import rsa
from Cryptographer import Cryptographer
from BBS import BBS

parser = argparse.ArgumentParser(description='Encryptor parser')
parser.add_argument('-i', type=str, default=r'source.wav')
parser.add_argument('-o', type=str, default=r'audio.wav')
parser.add_argument('-fmsg', type=str, default=None)
parser.add_argument('-msg', type=str, default="Hello world!")
parser.add_argument('-enc', type=str, default="utf-8")
args = parser.parse_args()

if args.fmsg is not None:
    with open(args.fmsg, "r") as read_text:
        msg = read_text.read().replace("\n", "*")
else:
    msg = args.msg

with open("public_key.txt", "r") as pr:
    private_str = pr.read().split(" ")
    public = rsa.PublicKey(int(private_str[0]), int(private_str[1]))

audio_test = Audio(filename=args.i)
audio = Audio(filename=args.i)
encrypter = Cryptographer(audio=audio, algorithm=BBS(), coding=args.enc)
encrypter.encrypt(msg, filename=args.o, publicKey=public)
audio2 = Audio(filename=args.o)
print("Successfully encrypted")
