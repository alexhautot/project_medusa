#!/usr/bin/env python3

import threading
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

import mathystuff as ms


# Initialising sensors and motors

# defining the 4 motors 
lf = LargeMotor(OUTPUT_A)
lr = LargeMotor(OUTPUT_B)
rf = LargeMotor(OUTPUT_C)
rr = LargeMotor(OUTPUT_D)

# Defining sensors and their output

gyro = sensors.GyroSensor()

front_ultra= sensors.UltrasonicSensor('in1')
front_ultra.mode='US-DIST-MS'
right_ultra= sensors.UltrasonicSensor('in2')
right_ultra.mode='US-DIST-MS'
up_ultra = = sensors.UltrasonicSensor('in3')
up_ultra.mode='US-DIST-MS'

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
    time.sleep(15)

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
    time.sleep(15)


# Forward function moves Medusa forward by approx 10 cm
def forward():
    rotes = 200
    forward_speed  = 200
    lr.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    lf.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    rf.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    rr.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    time.sleep(3)

# Forward function moves Medusa forward by approx 10 cm
def backward():
    rotes = -200
    forward_speed  = -200
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



grid_pos = [1,1]

orientation = 0
movements = {0: [0,1], 1:[1,0],3:[0,-1],4:[-1,0]}

a = np.zeros((400,400))

a[0,0] = 1
a[1,0] = 1
a[0,1] = 1

orientation = 0
movements = {0: [0,1], 1:[1,0],2:[0,-1],3:[-1,0]}


actions = [forward, turn_left, turn_right, backward]
numactions = len(actions)
action_names = (a.__name__ for a in actions)
