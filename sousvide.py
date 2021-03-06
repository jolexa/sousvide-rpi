import os
import glob
from time import sleep

import RPi.GPIO as io

import subprocess
from optparse import OptionParser
from datetime import datetime

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

io.setmode(io.BCM)
power_pin = 24
io.setup(power_pin, io.OUT)

def tempdata():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    #print lines[-1].strip().split("=")[-1]
    temp_mC = lines[-1].strip().split("=")[-1] # temp in milliCelcius
    temp_C = float(temp_mC) / 1000.0
    temp_f = temp_C * 9.0 / 5.0 + 32.0
    return temp_f

def logtemp( temp ):
    with open("temp.csv", "a") as myfile:
        myfile.write(datetime.now().time().isoformat() + "," + str(temp) + "\n")

def logpower( power ):
    with open("power.csv", "a") as myfile:
        myfile.write(datetime.now().time().isoformat() + "," + str(power) + "\n")

def setup_1wire():
  os.system("sudo modprobe w1-gpio && sudo modprobe w1-therm")

def turn_on():
    print(datetime.now().time().isoformat())
    io.output(power_pin, True)

def turn_off():
    print(datetime.now().time().isoformat())
    io.output(power_pin, False)

#Get command line options
parser = OptionParser()
parser.add_option("-t", "--target", type = int, default = 140)
parser.add_option("-p", "--prop", type = int, default = 6)
parser.add_option("-i", "--integral", type = int, default = 2)
parser.add_option("-b", "--bias", type = int, default = 40)
(options, args) = parser.parse_args()
print ('Target temp is %d' % (options.target))
target = options.target
P = options.prop
I = options.integral # I is a factor of the error that is carried forward
B = options.bias # Bias is the starting guess of % power on
# Initialise some variables for the control loop
interror = 0
pwr_cnt=1
pwr_tot=0

# Setup 1Wire for DS18B20
setup_1wire()

# Turn on for initial ramp up
state="on"
turn_on()

temperature=tempdata()
print("Initial temperature ramp up")
while (target - temperature > 4):
    sleep(15)
    temperature=tempdata()
    print("temp: " + str(temperature))
    logtemp(temperature)

print("Entering control loop")
while True:
    temperature=tempdata()
    print("temp: " + str(temperature))
    logtemp(temperature)
    error = target - temperature
    interror = interror + error
    power = B + ((P * error) + (I * interror))
    print("power: " + str(power))
    logpower(power)
    # Make sure that if power should be off then it is
    if (state=="off"):
        turn_off()
    # Long duration pulse width modulation
    for x in range (1, 100):
        if (power > x):
            if (state=="off"):
                state="on"
                print("On")
                turn_on()
        else:
            if (state=="on"):
                state="off"
                print("Off")
                turn_off()
        sleep(1)
