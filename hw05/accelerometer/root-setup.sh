#run this in root mode
su
cd /sys/class/i2c-adapter/i2c-2
echo adxl345 0x53 > new_device
