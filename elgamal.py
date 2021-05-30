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
    c2 = pow(pow(pk, r, p) * pow(m, 1, p), 1, p)
    return [c1,c2]

def decrypt(sk,c):
    m = pow((pow(c[1], 1, p)) * (pow(c[0], -sk, p)), 1, p)
    return m

