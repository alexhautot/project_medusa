#!/usr/bin/env python3


import datetime
#import numpy as np
import ev3dev2.sensor.lego as sensors
import ev3dev2.motor as motors
from ev3dev2.sound import Sound
from ev3dev.ev3 import Leds
import random
import os
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent

sound =Sound()


#flashy = Leds()


Leds.all_off()
def flashy():
    sound.speak('beep beep beep')
    for i in range(10):
        for group in (Leds.LEFT, Leds.RIGHT):
                Leds.set_color(group, Leds.YELLOW)
                time.sleep(0.5)
                Leds.all_off()

#flashy()

left_rear = LargeMotor(OUTPUT_A)

left_front = LargeMotor(OUTPUT_B)

right_front = LargeMotor(OUTPUT_C)

right_rear = LargeMotor(OUTPUT_D)

def forward():
    left_rear.on_for_rotations(SpeedPercent(-75),5)
    left_front.on_for_rotations(SpeedPercent(75),5)
    right_front.on_for_rotations(SpeedPercent(75),5)
    right_rear.on_for_rotations(SpeedPercent(-75),5)

forward()