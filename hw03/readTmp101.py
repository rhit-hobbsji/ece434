#!/usr/bin/env python3
#Read a TMP101 sensor
#//////////////////////////////////////
#Author : Jailen Hobbs
#Program: Reads from address 0x48 and 0x49 of I2C bus 2
#HArdware configuration to pins 19 and 20 with one TMP101 GND and one floating
#

import smbus
import time

#i2c bus and addresses
bus = smbus.SMBus(2)
address = 0x48
address2 = 0x49

while True:
	#Get temp of both TMP101 sensors
	temp = bus.read_byte_data(address, 0)
	temp2 = bus.read_byte_data(address2, 0)
	print(str(temp)+"-Sensor1 "+ str(temp2) + "-Sensor2", end = "\r")
	time.sleep(0.1)
