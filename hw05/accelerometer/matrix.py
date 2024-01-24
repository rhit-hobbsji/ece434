#!/usr/bin/env python3
# Etch SKetch with an 8x8 Red/Green LED matrix and Rotary Encoders and TMP101 sensors
#//////////////////////////////////////
#Author : Jailen Hobbs
#Program: Reads from address 0x48 and 0x49 and 0x70 of I2C bus 2
#Hardware i2c configuration to pins 19 and 20 with one TMP101 GND and one floating and a ocnnection to LCD matrix
#EQEP pins 33 and 35 are for left and right
#EQEP pins 41 and 42 are for up and down

import smbus
import time

bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
adxl345 = '53' # accelometer address in hex 

#i2c bus
i2cbus = '2'

path1 = '/sys/class/i2c-adapter/i2c-'+i2cbus+'/' + i2cbus + '-00' + adxl345 + '/iio:device0'

delay = 0.3; # Delay between images in s

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
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
    if(curCol < 0): curCol = 0
    array[curPos] = array[curPos] | pow(2, curCol)

def clear():
    print("clear")
    for i in range(len(array)):
        array[i] = 0x00

f = open(path1+'in_accel_x_raw', 'r')
f.seek(0)
xOldData = int(f.read())
f.close()
    
f = open(path1+'in_accel_y_raw', 'r')
f.seek(0)
yOldData = int(f.read())
f.close()

while True:
    # temp = bus.read_byte_data(tmp1, 0)
    # temp2 = bus.read_byte_data(tmp2, 0)
    
    #Set varaibles for both encoders l = left R - Right position of your encoders
    f = open(path1+'in_accel_x_raw', 'r')
    f.seek(0)
    xCurData = int(f.read())
    f.close()
    
    f = open(path1+'in_accel_y_raw', 'r')
    f.seek(0)
    yCurData = int(f.read())
    f.close()
    
    dx = xCurData - xOldData
    dy = yCurData - yOldData
    
    if(dx > 0):
        if(abs(dx) > 7):
            move_right()       
    elif(dx < 0):
        if(abs(dx) > 7):
            move_left()
    elif(dy > 0):
        if(abs(dy) > 7):
            move_right()       
    elif(dy < 0):
        if(abs(dy) > 7):
            move_down()
        
    xOldData = xCurData
    yOldData = yCurData 
    bus.write_i2c_block_data(matrix, 0, array)
    
    #debounce
    time.sleep(delay)

