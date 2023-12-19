#!/usr/bin/env python3
# Write an 8x8 Red/Green LED matrix
# https://www.adafruit.com/product/902

import smbus
import time

bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
tmp1 = 0x48 #sensor 1
tmp2 = 0x49 #Sensor 2

#SETUP EQEP 1 AND 2
eQEP1 = '1'
pathe1 = '/dev/bone/counter/' +eQEP1 + '/count0'

eQEP2 = '2'
pathe2 = '/dev/bone/counter/' +eQEP2 + '/count0'

delay = 0.1; # Delay between images in s

#Set Ceiling values
startCount = '5000'
maxCount = '10000'
f = open(pathe1+'/ceiling', 'w')
f.write(maxCount)
f.close()

f = open(pathe2+'/ceiling', 'w')
f.write(maxCount)
f.close()

f = open(pathe1+'/count', 'w')
f.write(startCount)
f.close()

f = open(pathe2+'/count', 'w')
f.write(startCount)
f.close()

#enable Rotaryencoders
f = open(pathe1+'enable', 'w')
f.write('1')
f.close()

f = open(pathe2+'enable', 'w')
f.write('1')
f.close()

#Set varaibles for both encoders l = left R - Right position of your encoders
l = open(pathe1+'/count', 'r')
r = open(pathe1+'/count', 'r')

horzEncoderOldData = 5000
horzEnoderCurData = 5000

vertEncoderOldData = 5000
vertEnoderCurData = 5000

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
array = [0x00, 0x3c, 0x00, 0x42, 0x28, 0x89, 0x04, 0x85,
    0x04, 0x85, 0x28, 0x89, 0x00, 0x42, 0x00, 0x3c
]

bus.write_i2c_block_data(matrix, 0, array)

while True:
    
    temp = bus.read_byte_data(tmp1, 0)
    temp2 = bus.read_byte_data(tmp2, 0)
    bus.write_i2c_block_data(matrix, 0, array)

