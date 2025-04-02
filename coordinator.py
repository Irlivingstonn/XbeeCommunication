# Borrowed code from: 
# https://www.digi.com/resources/documentation/digidocs/90001537/references/r_xbee_api_packets.htm?TocPath=Categories%7CCode%20Samples%7C_____44

# Imports
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
import serial
import sys
import binascii
import math  
import time  
import os

# XBee device configuration
PORT = "/dev/ttyUSB0"  # Change to your port
BAUD_RATE = 9600

# User Data <-- make sure to change when using
com_port = 'COM1'
dest_64bit = '0013A200422DBACE'
dest_16bit = 'FFFE'

# Covert png to hex
IMAGE_FILE = 'image9.png'
IMAGE_FILE = 'image9.png'

# Maximum bytes per packet (XBee has limits)
MAX_BYTES_PER_PACKET = 72




with open(IMAGE_FILE, 'rb') as f:
    rf_data = f.read()
# print(binascii.hexlify(rf_data))

def main():
    print("Starting Image Transfer...")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        # Open the device
        device.open()
        print(f"Connected to local XBee device: {device.get_64bit_addr()}")

        # Get the remote device
        remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(str(device.get_64bit_addr())))
        
        file_size = os.path.getsize(IMAGE_FILE)
        print(f"Image size: {file_size} bytes")

        # Read the image file
        with open(IMAGE_FILE, 'rb') as f:
            image_data = f.read()
        
        total_size = len(image_data)
        print(f"Image size: {total_size} bytes")
        
        # Calculate number of packets needed
        num_packets = (total_size + MAX_BYTES_PER_PACKET - 1) // MAX_BYTES_PER_PACKET
        print(f"Sending image in {num_packets} packets...")
        
        # Send image in chunks
        for i in range(0, total_size, MAX_BYTES_PER_PACKET):
            # Get chunk of data
            chunk = image_data[i:i+MAX_BYTES_PER_PACKET]
            
            # Send the data chunk
            print(f"Sending packet {i//MAX_BYTES_PER_PACKET + 1}/{num_packets} ({len(chunk)} bytes)")
            #device.send_data_broadcast(chunk)
            device._send_data_64_16(remote_device, chunk)
            

            delay = min(0.05, 0.01 + (len(chunk) / 5000))
            time.sleep(delay)


            
            
            # Small delay to prevent overwhelming the receiver
            time.sleep(0.1)


        device.close()


    except Exception as e:
        print(f"Error: {e}")

    finally:
        if device is not None and device.is_open():
            device.close()
            print("XBee device closed")


if __name__ == '__main__':
    main()





#def b_u(st):
#    ## function to convert big-endian binary string into bytes[0-1] as int
#    if len(st) == 1:
#         return ord(st)
#    else:
#        length = len(st)
#        sft = 8*(length-1)
#        return (b_u(st[0])<<sft) + b_u(st[1:])
#    
#
#
#
### create serial socket connection to talk with module
#ser = serial.Serial(com_port, 9600, timeout=0.1, rtscts=True)
#
#
### convert RF data to hex
#rf_hex = binascii.hexlify(rf_data)
###print "rf_hex=", rf_hex
#
#ceil_value  = math.ceil(rf_hex)
#
#
### calculate packet length
#hex_len = hex(14 + (len(ceil_value))/2)
#hex_len = hex_len.replace('x','0')
###print "hex_len=", hex_len
#
### calculate checksum
### 0x17 is the sum of all parameters minus 64bit & 16bit dest addr & payload
#checksum = 17
#
#
#for i in range(0,len(dest_64bit),2):
#    checksum = checksum + int(dest_64bit[i:i+2],16)
#
#for i in range(0,len(dest_16bit),2):
#    checksum = checksum + int(dest_16bit[i:i+2],16)
#
#for i in range(0,len(rf_hex),2):
#    checksum = checksum + int(rf_hex[i:i+2],16)
#
### checksum = 0xFF - 8-bit sum of bytes between the length and checksum
#checksum = checksum%256
#checksum = 255 - checksum
#checksum = hex(checksum)
#checksum = checksum[-2:]
#
### designing packet
#tx_req = ("7E" + hex_len + "10" + "01" + dest_64bit
#          + dest_16bit + "00" + "00" + rf_hex + checksum)
#print("Tx packet = ", tx_req)
#
### convert packet from hex to binary
#data = binascii.unhexlify(tx_req)
#
#
#
#
#device.open()
#
#
#
### send data on serial line to module
## ser.write(data)
#device.send_data_broadcast(data)
#
### listin COM port for response
## resp = ser.readline()
## 
## ## convert response from binary to int
## resp = b_u(resp)
## 
## ## convert response from int to hex
## resp = '%x' % resp
## hex_data = resp.upper()
## print("Response (in hex) = ", hex_data)
#
### close connection
#ser.close()
