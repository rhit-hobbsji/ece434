#!/usr/bin/env python3
# Etch SKetch with Python Flask local server 192.168.7.2:8081
#//////////////////////////////////////
#Author : Jailen Hobbs
#Program: Plays etch-sketch connected to bus2 of i2c with flask server

import smbus
from flask import Flask, render_template

app = Flask(__name__)

bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

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

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<action>")
def action(action):
    global curCol, curPos
    if action == "left":
        move_left()
    elif action == "right":
        move_right()
    elif action == "up":
        move_up()
    elif action == "down":
        move_down()
    elif action == "clear":
        clear()

    bus.write_i2c_block_data(matrix, 0, array)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

