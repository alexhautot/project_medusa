#!/usr/bin/env python3

import threading

from threading import Thread
import datetime
import numpy as np
import ev3dev2.sensor.lego as sensors
import ev3dev2.motor as motors
from ev3dev2.sound import Sound
from ev3dev.ev3 import Leds
from ev3dev2.sensor.lego import UltrasonicSensor
import random
import os
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from PIL import Image, ImageDraw
import socket

#import mathystuff as ms


# Initialising sensors and motors

# defining the 4 motors 
lf = LargeMotor(OUTPUT_A)
lr = LargeMotor(OUTPUT_B)
rf = LargeMotor(OUTPUT_C)
rr = LargeMotor(OUTPUT_D)

# Defining sensors and their output

gyro = sensors.GyroSensor()

front_ultra= sensors.UltrasonicSensor('in1')
#front_ultra.mode='US-DIST-MS'
right_ultra= sensors.UltrasonicSensor('in2')
#right_ultra.mode='US-DIST-MS'
#up_ultra = sensors.UltrasonicSensor('in3')
#up_ultra.mode='US-DIST-MS'

# turns medusa unit left - currently hard coded at 90 degrees
def left_turn():
    a = gyro.value()
    while  (gyro.value() > (a - 90)):    
        lf.run_forever(speed_sp=25)
        lr.run_forever(speed_sp=25)
        rf.run_forever(speed_sp=-25)
        rr.run_forever(speed_sp=-25)
    lf.run_forever(speed_sp=0)
    lr.run_forever(speed_sp=0)
    rf.run_forever(speed_sp=0)
    rr.run_forever(speed_sp=0)
    overshoot = a + gyro.value()
    print(overshoot)
    time.sleep(1)

# turns medusa unit right - currently hard coded at 90 degrees
def right_turn():
    a = gyro.value()
    while  (gyro.value() < (a + 90)):    
        lf.run_forever(speed_sp=-25)
        lr.run_forever(speed_sp=-25)
        rf.run_forever(speed_sp=25)
        rr.run_forever(speed_sp=25)
    lf.run_forever(speed_sp=0)
    lr.run_forever(speed_sp=0)
    rf.run_forever(speed_sp=0)
    rr.run_forever(speed_sp=0)
    overshoot = a + gyro.value()
    print(overshoot)
    time.sleep(1)


# Forward function moves Medusa forward by approx 10 cm
def forward():
    rotes = 200
    forward_speed  = 200
    lr.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    lf.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    rf.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    rr.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    time.sleep(3)

# Checks to see if there is a table to the right
# Uses front ultasonic sensor and the upwardly pointed sensor
# to test if there is a non-vertical surface present
# Powered by maths! 
def query_table():
    right_turn()
    val = 0
    if ms.is_wall(front_ultra.distance_centimeters, up_ultra.distance_centimeters) == 'desk':
        val = 1
    left_turn()
    return val

thread_bool = True

def beeeeeep():
    sound = Sound()
    while thread_bool:
        sound.speak('beep beep beep beep beep beep beep beep beep')

# Customer requested flashing lights and beeping to alert nearby people of it's operation 
def flashy():
    while thread_bool:
        Leds.all_off()
        for i in range(10):
            for group in (Leds.LEFT, Leds.RIGHT):
                    Leds.set_color(group, Leds.YELLOW)
                    time.sleep(0.5)
                    Leds.all_off()

print("testing beep")
sou = Thread(target=beeeeeep)
sou.start()

time.sleep(10)

print("testing flash")
fla = Thread(target=flashy)

fla.start()
time.sleep(10)

print("now flashing and beeping for remainder of tests.  You asked for this.")

print("testing forward motion")
forward()
time.sleep(10)

print("testing left turn")
left_turn()
time.sleep(10)

print("testing Right turn")
right_turn()
time.sleep(10)

print("testing object detection - will drive forward until it reaches an obsticle")
while front_ultra.distance_centimeters > 20:
    forward()
time.sleep(10)

thread_bool = false

print("tests completed")



