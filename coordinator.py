# Borrowed code from: 
# https://www.digi.com/resources/documentation/digidocs/90001537/references/r_xbee_api_packets.htm?TocPath=Categories%7CCode%20Samples%7C_____44

# Imports
import serial
import sys
import binascii

# User Data <-- make sure to change when using
com_port = 'COM1'
dest_64bit = '13A200422DBACE'
dest_16bit = 'FFFE'




# Covert png to hex
filename = 'death_star.png'
with open(filename, 'rb') as f:
    content = f.read()
print(binascii.hexlify(content))




def b_u(st):
    ## function to convert big-endian binary string into bytes[0-1] as int
    if len(st) == 1:
         return ord(st)
    else:
        length = len(st)
        sft = 8*(length-1)
        return (b_u(st[0])<<sft) + b_u(st[1:])
    



## create serial socket connection to talk with module
ser = serial.Serial(com_port, 9600, timeout=0.1, rtscts=True)


## convert RF data to hex
rf_hex = binascii.hexlify(rf_data)
##print "rf_hex=", rf_hex


## calculate packet length
hex_len = hex(14 + (len(rf_hex)/2))
hex_len = hex_len.replace('x','0')
##print "hex_len=", hex_len

## calculate checksum
## 0x17 is the sum of all parameters minus 64bit & 16bit dest addr & payload
checksum = 17


for i in range(0,len(dest_64bit),2):
    checksum = checksum + int(dest_64bit[i:i+2],16)

for i in range(0,len(dest_16bit),2):
    checksum = checksum + int(dest_16bit[i:i+2],16)

for i in range(0,len(rf_hex),2):
    checksum = checksum + int(rf_hex[i:i+2],16)

## checksum = 0xFF - 8-bit sum of bytes between the length and checksum
checksum = checksum%256
checksum = 255 - checksum
checksum = hex(checksum)
checksum = checksum[-2:]

## designing packet
tx_req = ("7E" + hex_len + "10" + "01" + dest_64bit
          + dest_16bit + "00" + "00" + rf_hex + checksum)
print("Tx packet = ", tx_req)

## convert packet from hex to binary
data = binascii.unhexlify(tx_req)

## send data on serial line to module
ser.write(data)

## listin COM port for response
resp = ser.readline()

## convert response from binary to int
resp = b_u(resp)

## convert response from int to hex
resp = '%x' % resp
hex_data = resp.upper()
print("Response (in hex) = ", hex_data)

## close connection
ser.close()
