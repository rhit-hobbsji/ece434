#!/usr/bin/env python3
# From: https://graycat.io/tutorials/beaglebone-io-using-python-mmap/
from mmap import mmap
import time, struct

# Modified by Jailen Hobbs

# Mapping the entire /dev/mem file would require that over a gigabyte be
# allocated in Python's heap, so the offset address and size variables are 
# used to keep the mmap as small as possible, in this case just the GPIO1 register. 
# These values are straight out of the memory map in section 2.1 of the 
# Technical Reference Manual. the GPIO_OE, GPIO_SETDATAOUT and GPIO_CLEARDATAOUT 
# addresses are found in section 25.4, which shows the address offsets of each 
# register within the GPIO modules, starting from the base module address. 
# Chapter 25 explains how to use the GPIO registers. 
# All we need to do is set a pin as an output, then set and clear its output state. 
# To do the first, we need the 'output enable' register (GPIO_OE above). 
# Then the GPIO_SETDATAOUT and GPIO_CLEARDATAOUT registers will do the rest. 
# Each one of these registers is 32 bits long, each bit of which corresponding 
# to one of 32 GPIO pins, so for pin 24 we need bit 24, or 1 shifted left 24 places.

GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
USR2 = 1 << 23
USR3 = 1 << 24

GPIO_DATAIN = 0x138
GPIO_DATAOUT = 0x13C

#P8_16 GPIO-1[14]
SW1 = 1 << 14

#P8_18 GPIO-2[1]
GPIO2_offset = 0x481A_C000
GPIO2_size = 0x481Acfff-GPIO2_offset
SW2 = 1 << 1


# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)

# The mmap is addressed byte by byte, so we can't just set a single bit. 
# The easiest thing to do is grab the whole 4-byte register:
packed_reg = mem[GPIO_OE:GPIO_OE+4]

# We now have 32 bits packed into a string, so to do any sort of bitwise operations with it we must unpack it:
# The 'L' tells struct.unpack() to unpack the string into an unsigned long, 
# which will give us the full 32-bit register. The '<' tells it that the 
# string is packed little-endian, or least-significant byte first. 
# The BeagleBone's memory is little-endian, so if we tell this to struct.unpack() 
# it will return the 32 bits in the order they are shown in the reference manual register maps.
reg_status = struct.unpack("<L", packed_reg)[0]

# We now have the 32-bit integer value of the register, so we can configure 
# the LED as an output by clearing its bit:
reg_status &= ~(USR3)
reg_status &= ~(USR2)
reg_status |= SW1

# Now all that's left to do is to pack it little-endian back into a string and update the mmap:

mem[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

# Now that we know the pin is configured as an output, it's time to get blinking. 
# We could use the GPIO_DATAOUT register to do this, 
# but we would want to preserve the state of all the other bits in it, 
# so we would need to do the same process of unpacking, manipulating then repacking. 
# That's what the SETDATAOUT and CLEARDATAOUT registers are for. 
# Writes to them affect only the pins whose bits are set to 1, making the next step much easier:

with open("/dev/mem", "r+b" ) as g:
  mem2 = mmap(g.fileno(), GPIO2_size, offset=GPIO2_offset)


packed_reg2 = mem2[GPIO_OE:GPIO_OE+4]

reg_status2 = struct.unpack("<L", packed_reg2)[0]
reg_status2 |= (SW2)

mem2[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status2)

try:
  while(True):
    gpio1_datain = mem[GPIO_DATAIN:GPIO_DATAIN + 4]
    gpio2_datain = mem2[GPIO_DATAIN:GPIO_DATAIN + 4]
    
    inp1_status = struct.unpack("<L", gpio1_datain)[0]
    inp2_status = struct.unpack("<L", gpio2_datain)[0]
    
    #print(str(inp2_status & (1<<1)) + "-" + str(SW2))
    #print(str(inp1_status & (1<<14)) + "-" + str(SW1))

    
    if(inp1_status & SW1):
      mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", USR3)
    else:
      mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", USR3)
    
    if(inp2_status & SW2):
       mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", USR2)
    else:
      mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", USR2)
    
    time.sleep(0.5)

except KeyboardInterrupt:
  mem.close()
  mem2.close()