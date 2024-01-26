##  Author - Jailen Hobbs - Homework 5 - Dr. Yoder ##
Folders hold seperate make files (can do make in folder but makes git nasty)

dual gpio holds Kernel-Module Part 2 code. cp dual_gpio.c and Makefile into exploringBB/extras/kernel/gpio_test for best results
Setup: 
gpioLED1 = 60;     // P9_12 (GPIO60)
gpioLED2 = 50;     // P9_14 (GPIO50)
gpioButton1 = 47;  // P8_15 (GPIO47)
gpioButton2 = 65;  // P8_18 (GPIO65)

gpio_test is in kernel_modules changed given gpio_test.c to work on pins P9_15 and P9_16 do makefile ad .c instructions above

make1 holds makefile from part1

dualLed folder holds toggling LEDs at different rates:  
GPIO output pins for LEDs P9_23 ,P9_24

Accelerometer data in accelerometer file
Am using accelerometer hooked to i2c-2 bus with address 0x53 (leave cs open)

# hw05 grading

| Points      | Description |
| ----------- | ----------- |
|  0/0 | Project 
|  2/2 | Makefile
|  5/6 | Kernel Source | Version missing.
|  6/6 | Kernel Modules: hello, ebbchar, gpio_test, led
|  4/4 | Etch-a-Sketch
|  2/2 | Blink at different rates
| 19/20 | **Total**

*My comments are in italics. --may*
