#!/usr/bin/env python3
# //////////////////////////////////////
#       getsetEvent.py
#   Like getset.py but uses events.
#   Get the value of P8_16 and write it to P9_14.
#     P8_16 is line 14 on chip 1.  P9_14 is line 18 of chip 1.
#       Wiring: Attach a switch to P8_16 and 3.3V and an LED to P9_14.
#       Setup:  sudo apt uupdate; sudo apt install libgpiod-dev
#           Run: gpioinfo | grep -i -e chip -e P9_14 to find chip and line numbers
#       See:    https://github.com/starnight/libgpiod-example/blob/master/libgpiod-led/main.c
# //////////////////////////////////////
# Based on https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/examples

import gpiod
import sys


def create_board():
    input1 = input("Enter Board size (NxN): ")
    size = int(input1)
    print("Board Size " + input1 + " x " + input1)

    global max_index, row, col, min_index
    row, col = 0, 0
    min_index = 0
    max_index = size - 1

    array = [["-" for i in range(size)] for k in range(size)]
    return array

def move_left():
    global row
    row = row - 1
    if (row < min_index):
        row = max_index

def move_right():
    global row
    row = row + 1
    if (row > max_index):
        row = min_index

def move_up():
    global col
    col = col - 1
    if (col < min_index):
        col = max_index

def move_down():
    global col
    col = col + 1
    if (col > max_index):
        col = min_index

def clear():
    global array
    for i in range(len(array)):
        for k in range(len(array)):
            array[i][k] = "-"
    

CONSUMER='getset'
CHIP='1'

# cleargetoffsets=[12] #P8_12
# leftgetoffsets=[10] # P8_14
# rightgetoffsets=[15] # P8_15
# upgetoffsets=[14] # P8_16
# downgetoffsets=[11] # P8_17
# leftsetoffests=[18] # P9_14
# rightsetoffests=[19] # P9_16
# upsetoffests=[9] # P8_13
# downsetoffests=[8] # P8_19
# clearsetoffsets=[31] # P8_26

#getoffsets = [12, 10, 15, 11, 14]
getoffsets = [12, 8, 15, 11, 14]
setoffsets = [18, 19, 9, 8, 31]




def print_event(event):
    if event.type == gpiod.LineEvent.RISING_EDGE:
        evstr = ' RISING EDGE'
    elif event.type == gpiod.LineEvent.FALLING_EDGE:
        evstr = 'FALLING EDGE'
    else:
        raise TypeError('Invalid event type')

    print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                           event.source.offset(),
                                                           event.sec, event.nsec))

chip = gpiod.Chip(CHIP)

getlines = chip.get_lines(getoffsets)
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)
# rgetlines = chip.get_lines(rightgetoffsets)
# rgetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)
# ugetlines = chip.get_lines(upgetoffsets)
# ugetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)
# dgetlines = chip.get_lines(downgetoffsets)
# dgetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)
# cgetlines = chip.get_lines(cleargetoffsets)
# cgetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

setlines = chip.get_lines(setoffsets)
setlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
# rsetlines = chip.get_lines(rightsetoffests)
# rsetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
# usetlines = chip.get_lines(upsetoffests)
# usetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
# dsetlines = chip.get_lines(downsetoffests)
# dsetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
# csetlines = chip.get_lines(clearsetoffsets)
# csetlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)

print("Hit ^C to stop")

global array
array = create_board()
x = 0

for r in array:
        for element in r:
            print(element, end=" ")
        print()

vals = []

while True:
    x = 0
    
    ev_lines = getlines.event_wait(sec=1)
    
    if ev_lines:
        for line in ev_lines:
            event = line.event_read()
            print_event(event)
    vals = getlines.get_values()
    
    
    for val in vals:
        print(val, end=' ')
    print('\r', end='')

    setlines.set_values(vals)
    
    if vals[0]:
        move_left()
    elif vals[1]:
        move_right()
    elif vals[2]:
        move_up()
    elif vals[3]:
        move_down()
    elif vals[4]:
        clear()
        x = 1
    
    if(x != 1):
        array[col][row] = "x" 
    
    # for r in array:
    #     for element in r:
    #         print(element, end=" ")
    #     print()
    print()
    