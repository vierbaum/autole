from gpiozero import AngularServo, PWMLED
import RPi.GPIO as GPIO
from time import sleep

servo = AngularServo(18)

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

motor = PWMLED(4)

#sleep(1)

def steer(direction):
    if direction == "r":
        servo.angle = 35
        sleep(0.5)
    elif direction == "l":
        servo.angle = -35
        sleep(0.5)
    else:
        servo.angle = 0
        sleep(0.5)


def drive(direction):
    if direction == 1:
        GPIO.output(2, GPIO.HIGH)
        GPIO.output(3, GPIO.LOW)
    else:
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.HIGH)
    motor.value = 1
    sleep(0.5)

def stop():
    motor.value = 0

