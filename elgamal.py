import random

from params import p
from params import g

def keygen():
    sk = random.randint(1, p)
    pk = pow(g, sk, p)
    return pk,sk

def encrypt(pk,m):
    r = random.randint(1, p)
    c1 = pow(g, r, p)
    hrm = pow(pk, r) * m
    c2 = pow(hrm, 1, p)
    return [c1,c2]

def decrypt(sk,c):
    m = c[1] * (pow(c[0], -sk, p))
    return m

