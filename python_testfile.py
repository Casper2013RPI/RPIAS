################
# Alarm System #
################
print ("Alarm")
if x= 0
then print ("Alarm")

#! /bin/bash 
15 echo "Welcome to Casper2013RPI Installer." 
16 echo " " 
17 echo "Requirements:" 
18 echo "1) Must be connected to the internet" 
19 echo "2) This script must be run as root user" 
20 echo " " 
21 echo "Steps:" 
22 echo "1) Installs package dependencies:" 
23 echo "   - python-pip       alternative Python package installer" 
24 echo "   - git              fast, scalable, distributed revision control system" 
25 echo "   - libi2c-dev       userspace I2C programming library development files" 
26 echo "   - python-serial    pyserial - module encapsulating access for the serial port" 
27 echo "   - python-rpi.gpio  Python GPIO module for Raspberry Pi" 
28 echo "   - i2c-tools        This Python module allows SMBus access through the I2C /dev" 
29 echo "   - python-smbus     Python bindings for Linux SMBus access through i2c-dev" 
30 echo "   - arduino          AVR development board IDE and built-in libraries" 
31 echo "   - minicom          friendly menu driven serial communication program" 
32 echo "2) Installs wiringPi in GrovePi/Script" 
33 echo "3) Removes I2C and SPI from modprobe blacklist /etc/modprobe.d/raspi-blacklist.conf" 
34 echo "4) Adds I2C-dev, i2c-bcm2708 and spi-dev to /etc/modules" 
35 echo "5) Installs gertboard avrdude_5.10-4_armhf.deb package" 
36 echo "6) Runs gertboard setup" 
37 echo "   - configures avrdude" 
38 echo "   - downloads gertboard known boards and programmers" 
39 echo "   - replaces avrsetup with gertboards version" 
40 echo "   - in /etc/inittab comments out lines containing AMA0" 
41 echo "   - in /boot/cmdline.txt removes: console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1" 
42 echo "   - in /usr/share/arduino/hardware/arduino creates backup of boards.txt" 
43 echo "   - in /usr/share/arduino/hardware/arduino creates backup of programmers.txt" 
44 echo " " 
45 echo "Special thanks to Joe Sanford at Tufts University. This script was derived from his work. Thank you Joe!" 
46 echo " " 
47 echo "Raspberry Pi wil reboot after completion." 
48 echo " " 
49 echo -e "Press \E[32mENTER\E[0m to begin... or \E[91mctrl+c\E[0m to abort" 
50 # read 
51 sleep 5 
52 
 
53 echo " " 
54 echo "Check for internet connectivity..." 
55 echo "==================================" 
56 wget -q --tries=2 --timeout=100 http://google.com 
57 if [ $? -eq 0 ];then 
58 	echo "Connected" 
59 else 
60 	echo "Unable to Connect, try again !!!" 
61 	exit 0 
62 fi 
63 
 
64 echo " " 
65 echo "Installing Dependencies" 
66 echo "=======================" 
67 sudo apt-get install python-pip git libi2c-dev python-serial i2c-tools python-smbus arduino minicom python-dev 
68 sudo apt-get purge python-rpi.gpio -y 
69 sudo apt-get purge python3-rpi.gpio -y 
70 sudo apt-get install python-rpi.gpio 
71 sudo apt-get install python3-rpi.gpio 
72 sudo pip install -U RPi.GPIO 
73 echo "Dependencies installed" 
74 
 
75 git clone git://git.drogon.net/wiringPi 
76 cd wiringPi 
77 ./build 
78 echo "wiringPi Installed" 
79 
 
80 echo " " 
81 echo "Removing blacklist from /etc/modprobe.d/raspi-blacklist.conf . . ." 
82 echo "==================================================================" 
83 if grep -q "#blacklist i2c-bcm2708" /etc/modprobe.d/raspi-blacklist.conf; then 
84 	echo "I2C already removed from blacklist" 
85 else 
86 	sudo sed -i -e 's/blacklist i2c-bcm2708/#blacklist i2c-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf 
87 	echo "I2C removed from blacklist" 
88 fi 
89 if grep -q "#blacklist spi-bcm2708" /etc/modprobe.d/raspi-blacklist.conf; then 
90 	echo "SPI already removed from blacklist" 
91 else 
92 	sudo sed -i -e 's/blacklist spi-bcm2708/#blacklist spi-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf 
93 	echo "SPI removed from blacklist" 
94 fi 
95 
 
96 #Adding in /etc/modules 
97 echo " " 
98 echo "Adding I2C-dev and SPI-dev in /etc/modules . . ." 
99 echo "================================================" 
100 if grep -q "i2c-dev" /etc/modules; then 
101 	echo "I2C-dev already there" 
102 else 
103 	echo i2c-dev >> /etc/modules 
104 	echo "I2C-dev added" 
105 fi 
106 if grep -q "i2c-bcm2708" /etc/modules; then 
107 	echo "i2c-bcm2708 already there" 
108 else 
109 	echo i2c-bcm2708 >> /etc/modules 
110 	echo "i2c-bcm2708 added" 
111 fi 
112 if grep -q "spi-dev" /etc/modules; then 
113 	echo "spi-dev already there" 
114 else 
115 	echo spi-dev >> /etc/modules 
116 	echo "spi-dev added" 
117 fi 
118 
 
119 echo " " 
120 echo "Making I2C changes in /boot/config.txt . . ." 
121 echo "================================================" 
122 
 
123 echo dtparam=i2c1=on >> /boot/config.txt 
124 echo dtparam=i2c_arm=on >> /boot/config.txt 
125 
 
126 sudo adduser pi i2c 
127 sudo chmod +x /home/pi/Desktop/GrovePi/Software/Scratch/GrovePi_Scratch_Scripts/*.sh 
128 
 
129 #Adding ARDUINO setup files 
130 echo " " 
131 echo "Making changes to Arduino . . ." 
132 echo "===============================" 
133 cd /tmp 
134 wget http://project-downloads.drogon.net/gertboard/avrdude_5.10-4_armhf.deb 
135 sudo dpkg -i avrdude_5.10-4_armhf.deb 
136 sudo chmod 4755 /usr/bin/avrdude 
137 
 
138 cd /tmp 
139 wget http://project-downloads.drogon.net/gertboard/setup.sh 
140 chmod +x setup.sh 
141 sudo ./setup.sh 
142 
 
143 echo " " 
144 echo "Install smbus for python" 
145 sudo apt-get install python-smbus 
146 
 
147 echo " " 
148 echo "Please restart to implement changes!" 
149 echo "  _____  ______  _____ _______       _____ _______ " 
150 echo " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|" 
151 echo " | |__) | |__  | (___    | |  /  \  | |__) | | |   " 
152 echo " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   " 
153 echo " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   " 
154 echo " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   " 
155 echo " " 
156 echo "Please restart to implement changes!" 
157 echo "To Restart type sudo reboot" 


Status
 API
 Training
 Shop
 Blog
 About
 Pricing
 Thank you foö r reading
