# coding=utf-8
from Crypto.Cipher import AES
import base64
import os


def encryption(privateInfo):
    BLOCK_SIZE = 16
    PADDING = '{'
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) *PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = '�{��z����m3nQ"�'
    print 'encryptionkey:', secret
    cipher = AES.new(secret)
    encoded = EncodeAES(cipher, privateInfo)
    print 'Encryptedstring:', encoded

encryption('some12_fna@gmail.com')