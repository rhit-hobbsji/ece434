#!/usr/bin/env python3
# Write an 8x8 Red/Green LED matrix
# https://www.adafruit.com/product/902

import smbus
import time
bus = smbus.SMBus(2)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
tmp1 = 0x48 #sensor 1
tmp2 = 0x49 #Sensor 2

delay = 1; # Delay between images in s

# bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
# bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
smile = [0x00, 0x3c, 0x00, 0x42, 0x28, 0x89, 0x04, 0x85,
    0x04, 0x85, 0x28, 0x89, 0x00, 0x42, 0x00, 0x3c
]

bus.write_i2c_block_data(matrix, 0, smile)
