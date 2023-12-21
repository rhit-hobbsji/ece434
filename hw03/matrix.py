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

delay = 0.3; # Delay between images in s

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

#initial rotary numbers
horzEncoderOldData = 5000
horzEncoderCurData = 5000
vertEncoderOldData = 5000
vertEncoderCurData = 5000

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
array = [0x01, 0x00, 0x02, 0x00, 0x04, 0x00, 0x08, 0x00,
    0x10, 0x00, 0x20, 0x00, 0x40, 0x00, 0x80, 0x00
]

curCol = 0
curPos = 0 #curRow

bus.write_i2c_block_data(matrix, 0, array)

def move_left():
    print("left")
    global curPos 
    if(curPos < 1): return 
    curPos = curPos - 2
    array[curPos] = array[curPos] | (pow(2, curCol))
    
    
def move_right():
    print("right")
    global curPos 
    if(curPos > 15): return
    curPos = curPos + 2
    array[curPos] = array[curPos] | (pow(2, curCol))
    

def move_up():
    print("up")
    global curCol
    curCol = curCol + 1
    if(curCol > 7): curCol = 0
    array[curPos] = array[curPos] | pow(2, curCol)

def move_down():
    print("down")
    global curCol
    curCol = curCol - 1
    
    array[curPos] = array[curPos] | pow(2, curCol)

def clear():
    print("clear")
    for i in range(len(array)):
        array[i] = 0x00

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
    
    if(horzData > 0):
        move_right()
    elif (horzData < 0):
        move_left()
    elif(vertData > 0):
        move_up()
    elif(vertData < 0):
        move_down()   
     
    print(temp)
    print(temp2)
    if(temp > 28) | (temp2 > 28):
        print("TOO HOT GAME OVER INPUTS STUCK")
        break
    
    bus.write_i2c_block_data(matrix, 0, array)
    vertEncoderOldData = vertEncoderCurData
    horzEncoderOldData = horzEncoderCurData
    
    time.sleep(delay)

