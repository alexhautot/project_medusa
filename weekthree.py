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


# initialises values for grid walking  - an array of zeros to write to
# Medusa starts at position 1,1 and must be placed in a corner the zeroth
# will be walls

# orientation will be one of 4 directions in an x y plane as the Medusa unit
# only turns at right angles presently

grid_pos = [1,1]


orientation = 0
movements = {0: [0,1], 1:[1,0],3:[0,-1],4:[-1,0]}

a = np.zeros((40,40))

a[0,0] = 1
a[1,0] = 1
a[0,1] = 1

orientation = 0
movements = {0: [0,1], 1:[1,0],2:[0,-1],3:[-1,0]}



fla = Thread(target=flashy)

sou = Thread(target=beeeeeep)
sou.start()
fla.start()
#takes orientation and position and moves then adjusts grid based on what it sees

def move(orientation,grid_pos, a):
    forward()
    
    mov = movements[orientation]
    grid_pos[0]+=mov[0]
    grid_pos[1]+=mov[1]
    if right_ultra.distance_centimeters < 20 :
        a[grid_pos[0]-1,grid_pos[1]] = 1
    #if right_ultra.distance_centimeters > 20 :
    #    if query_table() == 1:
    #        a[grid_pos[0]-1,grid_pos[1]] = 2
    if front_ultra.distance_centimeters > 20:
        a[grid_pos[0]+mov[0],grid_pos[1]+mov[1]]=1
    return a
    

# Takes orientation and position and performs a left turn on map and in the flesh
def left_function(orientation, grid_pos):
    orientation = orientation + 1
    if orientation == 4:
        orientation = 0
    left_turn()
    return orientation 

# Takes orientation and position and performs a right turn on map and in the flesh
def right_function(orientation, grid_pos):
    orientation -=1
    if orientation == -1:
        orientation = 3
    right_turn()
    return orientation

def draw_that_map(map):
    im = Image.new('RGB', (500,400), color = 'blue')
    d = ImageDraw.Draw(im)
    d.text((10,10), 'blue prince', fill = 'white')
    d.text((10,30), 'scale = 1cm = 1px', fill = 'white')
    for i in range(1,(map.shape[0]-1)):
        x = i*10 +100
        for j in range(1,(map.shape[1]-1)):

            y = j*10
            if (map[i,j] == 1 and (map[i-1,j]==1 or map[i+1,j]==1)):
                draw = ImageDraw.Draw(im)
                draw.line((x, y) + (x+10,y), fill='white')
            if (map[i,j] == 1 and (map[i,j-1]==1 or map[i,j+1]==1)):
                draw = ImageDraw.Draw(im)
                draw.line((x, y) + (x,y+10), fill='white')
        
    im.save('blue_prints.png')


for i in range(0):
    while front_ultra.distance_centimeters > 20 and right_ultra.distance_centimeters < 20:
        a = move(orientation,grid_pos)
    
    
    if front_ultra.distance_centimeters < 20 :
        orientation = left_function(orientation,grid_pos)
        print('Orientation')
        print(orientation)
    
    #if front_ultra.distance_centimeters > 20 and right_ultra.distance_centimeters > 20:
    #    move(orientation,grid_pos)
    #    
    #    right_function(orientation,grid_pos)
    #    move(orientation,grid_pos)
    #    move(orientation,grid_pos)


draw_that_map(a)



#def inspect_walls():
#    if side_sens.distance_centimetres <20:

thread_bool = False 