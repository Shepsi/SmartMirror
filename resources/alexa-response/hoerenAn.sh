#!/bin/bash
gpio write 1 1
truncate -s 0 /home/pi/Smartmirror/alexa-response/ausgabe.txt
echo "hoerenAn" >> /home/pi/Smartmirror/alexa-response/ausgabe.txt