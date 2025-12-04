#!/usr/bin/python3
import os
import time
import subprocess
import time
import pygame
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_PIR = 12
GPIO.setup(GPIO_PIR,GPIO.IN)

num=0
status0 = 0
status1 = 0
try :
    while True:
              status0 = 0
              print ("Listo para comenzar!")
              while True:
                        status0 = GPIO.input(GPIO_PIR)
                        if status0==1 and status1==0:
                                     num=num+1
                                     archivo = "/home/uth/Desktop/ProyectoFinalEmbebida/lecturas-estados/sensor-pir.txt"
                                     with open(archivo, "w") as f:
                                         f.write(f"Movimiento detectado: {num}\n")
                                     status1=1
                        elif status0==0 and status1==1:
                                     print ("Listo para comenzar!")
                                     status1=0
                                     time.sleep(0.01)
except KeyboardInterrupt:
       GPIO.cleanup()
