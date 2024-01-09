#Configuration to remove defaule beagle LED usage
#Run this before running sudo ./dualSwitch.py or sudo ./gpioToggle.py
cd /sys/class/leds/beaglebone\:green\:usr3
echo none > trigger
echo 1 > brightness

cd /sys/class/leds/beaglebone\:green\:usr2
echo none > trigger
echo 1 > brightness