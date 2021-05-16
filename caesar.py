
def encrypt(key,plaintext):
    ciphertext=""
    #YOUR CODE HERE
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for t in plaintext:
        i = 0
        while t != alphabet[i]:
            i += 1
        j = (i+key) % 26
        ciphertext += alphabet[j]
    return ciphertext

def decrypt(key,ciphertext):
    plaintext=""
    #YOUR CODE HERE
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for t in ciphertext:
        i = 0
        while t != alphabet[i]:
            i += 1
        j = (i-key) % 26
        plaintext += alphabet[j]
    return plaintext


