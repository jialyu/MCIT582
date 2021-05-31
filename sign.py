from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256

import random

def sign(m):
    #generate public key
    #Your code here
    G = secp256k1.G
    n = secp256k1.q
    private_key, public_key = keys.gen_keypair(curve.secp256k1)
    
    #generate signature
    #Your code here
    r = pow(secp256k1.gx, 1, n)

    z = int(sha256(m.encode('utf8')).hexdigest(), 16)
    k = random.randint(1, n)
#   ss = pow(k, -1)*(z+r*private_key)
    # s = pow(ss, 1, n)
    s = pow(pow(k, -1, n)*(pow(z, 1, n) + pow(pow(r,1,n)*pow(private_key,1,n), 1, n)),1,n)
    
    assert isinstance( public_key, point.Point )
    assert isinstance( r, int )
    assert isinstance( s, int )
    return( public_key, [r,s] )
