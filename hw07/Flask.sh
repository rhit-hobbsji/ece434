## Set up for flash to boot on system start

sudo cp flask.service /lib/systemd/system
sudo systemctl enable flask

## Sudo reboot yourself and go to http://192.168.7.2:8081
