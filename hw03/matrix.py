#!/usr/bin/env python3
# Write an 8x8 Red/Green LED matrix
# https://www.adafruit.com/product/902

import smbus
import time

def move_left():
    print("left")

def move_right():
    print("right")

def move_up():
    print("up")

def move_down():
    print("down")

def clear():
    print("clear")

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
f = open(pathe1+'/enable', 'w')
f.write('1')
f.close()

f = open(pathe2+'/enable', 'w')
f.write('1')
f.close()

horzEncoderOldData = 5000
horzEncoderCurData = 5000

vertEncoderOldData = 5000
vertEncoderCurData = 5000

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
array = [0x00, 0x3c, 0x00, 0x42, 0x28, 0x89, 0x04, 0x85,
    0x04, 0x85, 0x28, 0x89, 0x00, 0x42, 0x00, 0x3c
]

curPos = [0x0,1]

bus.write_i2c_block_data(matrix, 0, array)

while True:
    temp = bus.read_byte_data(tmp1, 0)
    temp2 = bus.read_byte_data(tmp2, 0)
    
    #Set varaibles for both encoders l = left R - Right position of your encoders
    l = open(pathe1+'/count', 'r')
    l.seek(0)
    horzEncoderCurData = int(l.read())
    l.close()
    
    r = open(pathe2+'/count', 'r')
    r.seek(0)
    vertEncoderCurData = int(r.read())
    r.close()
    
    horzData = (horzEncoderCurData - horzEncoderOldData)
    vertData = (vertEncoderCurData - vertEncoderOldData)
    
    print(vertData)
    print(horzData)
    if(horzData > 0):
        move_right()
    elif (horzData < 0):
        move_left()
    elif(vertData > 0):
        move_up()
    elif(vertData < 0):
        move_down()   
     
    if(temp > 28) | (temp2 > 28):
        print("TOO HOT GAME OVER INPUTS STUCK")
        break
    
    bus.write_i2c_block_data(matrix, 0, array)
    vertEncoderOldData = vertEncoderCurData
    horzEncoderOldData = horzEncoderCurData
    
    time.sleep(0.3)

