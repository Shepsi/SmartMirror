#!/bin/bash
gpio write 4 0
truncate -s 0 /home/pi/Smartmirror/alexa-response/ausgabe.txt
echo "redenAus" >> /home/pi/Smartmirror/alexa-response/ausgabe.txt

