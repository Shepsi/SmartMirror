#!/bin/bash
gpio write 4 1
truncate -s 0 /home/pi/Smartmirror/alexa-response/ausgabe.txt
echo "redenAn" >> /home/pi/Smartmirror/alexa-response/ausgabe.txt

