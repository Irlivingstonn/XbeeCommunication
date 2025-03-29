import binascii
filename = 'death_star.png'
with open(filename, 'rb') as f:
    content = f.read()
print(binascii.hexlify(content))