#!/bin/bash

TRIG=23
ECHO=24

gpio -g mode $TRIG out
gpio -g mode $ECHO in

while true; do
    gpio -g write $TRIG 1
    sleep 0.00001   # 10 microsegundos
    gpio -g write $TRIG 0

    while [ "$(gpio -g read $ECHO)" -eq 0 ]; do :; done
    START_TIME=$(date +%s.%N)

    while [ "$(gpio -g read $ECHO)" -eq 1 ]; do :; done
    END_TIME=$(date +%s.%N)

    TIME_DIFF=$(echo "$END_TIME - $START_TIME" | bc)

    DISTANCE=$(echo "scale=2; ($TIME_DIFF * 17150) / 2" | bc)

    echo "Distancia: $DISTANCE cm" > /home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-ultrasonico.txt

    sleep 1
done
