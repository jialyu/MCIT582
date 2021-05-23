import hashlib
import os

def hash_collision(k):
    if not isinstance(k,int):
        print( "hash_collision expects an integer" )
        return( b'\x00',b'\x00' )
    if k < 0:
        print( "Specify a positive number of bits" )
        return( b'\x00',b'\x00' )
   
    #Collision finding code goes here
#     x = b'\x00'
#     y = b'\x00'
    c = 0
    while (c < k): 
        x = hashlib.sha256(os.urandom(16))
        y = hashlib.sha256(os.urandom(16))
        x_bits = ''
        y_bits = ''
        for i in range(len(x.digest())):
            x_bits += bin(x.digest()[i])[2:].zfill(8)
        for i in range(len(y.digest())):
            y_bits += bin(y.digest()[i])[2:].zfill(8)
        length = min(len(x_bits), len(y_bits))
        j = -1
        c = 0
        while (j>=-length): 
            if (x_bits[j] == y_bits[j]): 
                c += 1
                j -= 1
            else: 
#                 print(c)
                break
            
    # print(c)
    # print(x_bits)
    # print(y_bits)
    return( x.digest(), y.digest() )