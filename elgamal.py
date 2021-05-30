import random

from params import p
from params import g

def keygen():
    sk = random.randint(1, p)
    pk = (g^sk) % p
    return pk,sk

def encrypt(pk,m):
    q = (p-1)/2
    r = random.randint(1, q)
    c1 = (g^r) % p
    c2 = (pk^r) % m
    return [c1,c2]

def decrypt(sk,c):
    m = c[1]/(c[0]^sk) % p
    return m

