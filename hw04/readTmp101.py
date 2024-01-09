#!/usr/bin/env python3
#Reads 2 TMP101 sensor
#//////////////////////////////////////
#Author : Jailen Hobbs
#Program: Reads from address 0x48 and 0x49 of I2C bus 2 with kernel
#HArdware configuration to pins 19 and 20 with one TMP101 GND and one floating
#
import time

#enter dec value for ex address 0x48 put in 48
hAddr = '48'
hAddr2 = '49'

#i2c bus
i2cbus = '2'

path1 = '/sys/class/i2c-adapter/i2c-'+i2cbus+'/' + i2cbus + '-00' + hAddr + '/hwmon/hwmon0'
path2 = '/sys/class/i2c-adapter/i2c-'+i2cbus+'/' + i2cbus + '-00' + hAddr2 + '/hwmon/hwmon0'

delay = 0.3

while True:
	#Get temp of both TMP101 sensors
    f = open(path1, 'r')
    f.seek(0)
    temp = int(f.read)
    f.close()
    f = open(path2, 'r')
    f.seek(0)
    temp2 = int(f.read)
    f.close()
    print(str(temp)+"-Sensor1 "+ str(temp2) + "-Sensor2", end = "\r")
    time.sleep(delay)
