import hashlib
import os

def hash_preimage(target_string):
    if not all( [x in '01' for x in target_string ] ):
        print( "Input should be a string of bits" )
        return b'\x00'
    nonce_bits = ''
    while (nonce_bits[-len(target_string):] != target_string):
        nonce = hashlib.sha256(os.urandom(16))
        # nonce_bits = ''
        # for i in range(len(nonce.digest())):
        #     nonce_bits += bin(nonce.digest()[i])[2:].zfill(8)
        nonce_bits = bin(int(nonce.hexdigest(), 16))
    # print(nonce_bits)
    return( nonce.digest() )