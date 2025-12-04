import adafruit_dht
import board
from datetime import datetime
import time

dht_device = adafruit_dht.DHT11(board.D26)
file_path = "/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-dht11.txt"

try:
    while True:
        try:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                with open(file_path, "w") as file:
                    #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write(f"Temp: {temperature_c}C, Humedad: {humidity}%\n")
                print(f"Datos guardados en {file_path}")

            time.sleep(2)

        except RuntimeError as e:
            print(f"Error leyendo el sensor: {e}")
            time.sleep(1)  # Esperar un segundo y volver a intentar

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    dht_device.exit()
