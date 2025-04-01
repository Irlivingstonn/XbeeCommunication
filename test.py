# Imports
import sys
import binascii
import math 

filename = 'death_star.png'
with open(filename, 'rb') as f:
    rf_data = f.read()
print(binascii.hexlify(rf_data))
#rf_hex = binascii.hexlify(rf_data)

#hex_len1 = 14 + (len(rf_hex))/2


#ceil_value  = math.ceil(rf_hex)
#hex_len2 = 14 + (len(ceil_value))/2

#print("Result" + str(hex_len1) + " " + str(hex_len2))
