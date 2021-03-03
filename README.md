# ee101-rPi3Bp-sensehat-py

to enable sense-hat, I needed to append the following to my /boot/config.txt file

$ sudo nano /boot/config.txt

...then append
dtoverlay=rpi-sense

#ctl-o to save
#ctl-x to exit

$ sudo init 6
#to reboot
