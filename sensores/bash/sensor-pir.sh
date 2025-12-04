#!/bin/bash

# Configuración de los pines GPIO
gpio -g mode 12 in

movement_count=0
prev_status=0

while true; do
	current_status=$(gpio -g read 12)
	if [ "$current_status" = 1 ] && [ "$prev_status" = 0 ]; then
		movement_count=$((movement_count + 1))
		echo "Movimiento detectado: $movement_count" > /home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-pir.txt
		prev_status=1
		echo "1"
	elif [ "$current_status" = 0 ] && [ "$prev_status" = 1 ]; then
		echo "Listo para comenzar!"
		prev_status=0
	fi
	sleep 0.01
done
