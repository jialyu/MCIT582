import math

def num_BTC(b):
    mod = b % 210000
    div = b // 210000
    c = 0
    for d in range(0, div): 
        t = 2**d
        c += 210000 * (50/t)
    c += mod * (50/(2**div))
    return c