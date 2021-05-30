from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256

def sign(m):
	#generate public key
	#Your code here
    G = secp256k1.G
    n = secp256k1.q
    d = random.randint(1, secp256k1.q)
	private_key, public_key = fastecdsa.keys.gen_keypair(curve=secp256k1)

	#generate signature
	#Your code here
	r = pow(secp256k1.gx, 1, n)
    z = sha256(m)
    ss = pow(k, -1)*(z+r*d)
	s = pow(ss, 1, n)

	assert isinstance( public_key, point.Point )
	assert isinstance( r, int )
	assert isinstance( s, int )
	return( public_key, [r,s] )


