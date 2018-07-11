#!/bin/bash
gpio write 1 0
truncate -s 0 /home/pi/Smartmirror/alexa-response/ausgabe.txt
echo "hoerenAus" >> /home/pi/Smartmirror/alexa-response/ausgabe.txt

