#!/bin/bash
sox -t alsa hw:Loopback,1,0 -t wav -b 16 -c 1 -r 22050 - | sudo ./PiFmDma/PiFmDma /dev/stdin 100.0 > /dev/null 2>&1
