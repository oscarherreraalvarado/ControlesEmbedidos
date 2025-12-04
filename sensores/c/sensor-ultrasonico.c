#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <wiringPi.h>

#define TRIG 23
#define ECHO 24

int main() {
    if (wiringPiSetupGpio() == -1) {
        printf("Error al configurar GPIO\n");
        return 1;
    }

    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    FILE *file = NULL;
    long start_time;
    long end_time;

    while (1) {
        digitalWrite(TRIG, HIGH);
        usleep(10);
        digitalWrite(TRIG, LOW);

        while (digitalRead(ECHO) == LOW) {
            start_time = micros();
        }

        while (digitalRead(ECHO) == HIGH) {
            end_time = micros();
        }

        long time_diff = end_time - start_time;

        float distance = (time_diff * 0.0343) / 2;

        char message[100];
        snprintf(message, sizeof(message), "Distancia: %.2f cm\n", distance);

        file = fopen("/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-ultrasonico.txt", "w");
        if (file == NULL) {
            printf("Error al abrir el archivo\n");
            return 1;
        }

        fputs(message, file);

        fclose(file);

        sleep(1);
    }

    fclose(file);

    return 0;
}
