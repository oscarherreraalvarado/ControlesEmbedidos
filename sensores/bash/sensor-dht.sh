#!/bin/bash

DHTPIN=4
OUTPUT_FILE="/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-dht11.txt"

echo "Raspberry Pi wiringPi DHT11 Temperature test program"

gpio mode $DHTPIN out
gpio write $DHTPIN 0
sleep 0.018
gpio write $DHTPIN 1
sleep 0.4
gpio mode $DHTPIN in

read_dht11_data() {
    local data=()
    local bit_count=0
    local last_state=1
    local counter=0
    local i=0
    
    for ((i=0; i<85; i++)); do
        counter=0
        while [[ $(gpio read $DHTPIN) -eq $last_state ]]; do
            counter=$((counter+1))
            sleep 0.000001
            if [[ $counter -eq 255 ]]; then
                break
            fi
        done
        last_state=$(gpio read $DHTPIN)
        if [[ $counter -eq 255 ]]; then
            break
        fi
        if [[ $i -ge 4 && $((i % 2)) -eq 0 ]]; then
            data+=("$counter")
            bit_count=$((bit_count+1))
        fi
    done
    
    if [[ $bit_count -ge 40 ]]; then
        local humidity=$((data[0]))
        local temperature=$((data[2]))
        echo "Temp: ${temperature}C, Humedad: ${humidity}%"
    else
        echo "Data not good, skip"
    fi
}

while true; do
    read_dht11_data
    sleep 1
done

