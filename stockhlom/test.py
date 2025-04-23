#!/usr/bin/env python3
import os
import argparse
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt (key,filename):
    try:
        cipher = AES.new(key,AES.MODE_CBC)
        with open(filename,"rb") as f:
            data=f.read()
        ciphertext = cipher.encrypt(pad(data,AES.block_size))
        with open(filename+".ft","wb") as f:
            f.write(cipher.iv)
            f.write(ciphertext)
        # os.remove("filename")
    except Exception as e:
        print(f"error while encrypting")

def decrypt (key,filename):
    try:
        with open(filename,'rb') as f:
            iv = f.read(16)
            ciphertext= f.read()
        cipher = AES.new(key,AES.MODE_CBC,iv)
        plaintext = unpad(cipher.decrypt(ciphertext),AES.block_size)
    except Exception as e:
        print(f"error decrypting")


def main():
    filename="/home/fbicandy/42/infection/important.txt"
    encrypt(os.urandom(16),filename)
    # print(ciphertext)

