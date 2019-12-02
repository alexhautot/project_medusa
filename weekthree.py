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
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank

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

gyro = sensors.GyroSensor()


def left_turn():
    a = gyro.value()
    while  (gyro.value() > (a - 90)):    
        left_front.run_forever(speed_sp=100)
        left_rear.run_forever(speed_sp=-100)
        right_front.run_forever(speed_sp=-100)
        right_rear.run_forever(speed_sp=100)
    left_front.run_forever(speed_sp=0)
    left_rear.run_forever(speed_sp=0)
    right_front.run_forever(speed_sp=0)
    right_rear.run_forever(speed_sp=0)
    


def forward():
    left_rear.run_to_rel_pos(position_sp=-720, speed_sp=-450, stop_action="brake")
    left_front.run_to_rel_pos(position_sp=720, speed_sp=450, stop_action="brake")
    right_front.run_to_rel_pos(position_sp=720, speed_sp=450, stop_action="brake")
    right_rear.run_to_rel_pos(position_sp=-720, speed_sp=-450, stop_action="brake")
    
#tank_front =MoveTank(OUTPUT_B,OUTPUT_C)
#tank_rear = MoveTank(OUTPUT_A, OUTPUT_D)
#tank_front.on_for_seconds(SpeedPercent(75), SpeedPercent(75),5)
#tank_rear.on_for_seconds(SpeedPercent(-75), SpeedPercent(-75),5)

left_turn()