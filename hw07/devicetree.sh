## Setup for P9_14 driver to be enabled
sudo cp BB-W1-P9.14-00A0.dts /opt/source/bb.org-overlays/src/arm/
cd /opt/source/bb.org-overlays
sudo make && sudo make install

echo 'edit /boot/uEnv.txt to point to your new device'
