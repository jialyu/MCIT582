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
    while (c != k): 
        x = os.urandom(16)
        x_hash = hashlib.sha256(x)
        y = os.urandom(16)
        y_hash = hashlib.sha256(y)
#         x_bits = ''.join(format(ord(i), '08b') for i in x.hexdigest())
#         y_bits = ''.join(format(ord(i), '08b') for i in y.hexdigest())
        x_bits = bin(int(x_hash.hexdigest(), 16))
        y_bits = bin(int(y_hash.hexdigest(), 16))
#         x_bits = ''
#         y_bits = ''
#         for i in range(len(x.digest())):
#             x_bits += bin(x.digest()[i])[2:].zfill(8)
#         for i in range(len(y.digest())):
#             y_bits += bin(y.digest()[i])[2:].zfill(8)
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
    return( x, y )