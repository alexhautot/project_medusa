#!/usr/bin/env python3

import threading
import datetime
#import numpy as np
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


sound = Sound()


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

lf = LargeMotor(OUTPUT_A)

lr = LargeMotor(OUTPUT_B)

rf = LargeMotor(OUTPUT_C)

rr = LargeMotor(OUTPUT_D)

medusa_forward = MoveTank(OUTPUT_A, OUTPUT_C)

medusa_rear = MoveTank(OUTPUT_B, OUTPUT_D)


gyro = sensors.GyroSensor()

#ultra = UltrasonicSensor('in1')

front_ultra= sensors.UltrasonicSensor('in1')
#front_ultra.mode='US-DIST-MS'
right_ultra= sensors.UltrasonicSensor('in2')

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


rotes = 200
forward_speed  = 200
# Forward function moves Medusa forward by approx 10 cm
def forward():
        
    lr.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    lf.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    rf.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    rr.run_to_rel_pos(position_sp=rotes, speed_sp=forward_speed, stop_action="brake")
    time.sleep(3)

    

left_turn()


right_turn()



#while front_ultra.distance_centimeters > 20:
#    forward()

#

grid_position = [1,1]

#a = np.zeros((40,40))

#a[0,0] = 1
#a[1,0] = 1
#a[0,1] = 1



#def inspect_walls():
#    if side_sens.distance_centimetres <20:

