"""
Main program for profiler processor, gathers data, goes to surface, relays data, returns under ocean, loops

Radio code from: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi

Author: Nicholas Nguyen, Srushty Changela, Celeste Smith
"""
#!/usr/bin/env python3
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x
import serial
import RPi.GPIO as GPIO     
from time import sleep
import struct
import re

# Initialize motor
in1 = 27
in2 = 16
en = 17

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

timeUnderwater = 30
depth = 10

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# draw a box to clear the image
display.fill(0)
display.show()

# initialize lists
compassList = []
bmsList = []

'''
function to read information from the sensors while the profiler is "underwater"
returns lists of the data gathered from the compass and BMS
'''
def readSensor() -> [list, list]:
    compassList.clear()
    bmsList.clear()
    #open serial interface, could probably be moved outside this function
    serCompass = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
    serBMS = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
    #serCompass.flush()
    #serBMS.flush()
    #collect data for x seconds
    t_end = time.time() + timeUnderwater
    # TODO a much needed future improvement would be to make threads do the listening 
    while time.time() < t_end:
        # if there is something to read, read it
        # TODO: add error checking when collecting the data (like checking the checksums/CRCs)
        if serBMS.in_waiting > 0:
            lineBMS = serBMS.readline().rstrip()
            # append the new reading to the end of the list
            bmsList.append(lineBMS)
            print("diyBMS line read ", lineBMS)
        if serCompass.in_waiting > 0:
            lineCompass = serCompass.readline().rstrip()
            # append the new reading to the end of the list
            compassList.append(lineCompass)
            print("Compass line read", lineCompass)
        # read diyBMS again because two different lines are being send (temp and voltage)
        if serBMS.in_waiting > 0:
            lineBMS = serBMS.readline().rstrip()
            # append the new reading to the end of the list
            bmsList.append(lineBMS)
            print("diyBMS line read ", lineBMS)
        # collect information every 8 seconds
        time.sleep(8)
    return compassList, bmsList

# main loop for going through the sequence of profiler states
while True:
    packet = None
    print("///////////////////////////////////////////////////////////")
    # Step 1: read sensor data
    print("Reading compass/diyBMS data")
    display.fill(0)
    display.text('Reading data!', 25, 15, 1)
    display.show()
    compass_list, bms_list = readSensor()
    
    # Step 2: recall
    print("Recalling profiler")
    display.fill(0)
    display.text('Recalling', 25, 15, 1)
    display.show()
    # strange issues with the motor so this technique was developed
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    t_end = time.time() + depth
    while time.time() < t_end:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
    time.sleep(1)
    print("Surfaced")
    display.fill(0)
    display.text('Surfaced', 25, 15, 1)
    display.show()
    # stop motor
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    time.sleep(1)
    
    # Step 3: send through radio
    print("Sending data through radio")
    display.fill(0)
    display.text('Sending data', 25, 15, 1)
    display.show()
    # iterate through and send compass list of data
    for c in range(0, len(compass_list)):
        if len(compass_list[c]) != 0:
            rfm9x.send(compass_list[c])
            #time.sleep(3)
    # flag to show compass data is done being sent
    rfm9x.send(bytes("1", "utf-8"))
    time.sleep(3)
    # iterate through and send bms data
    for b in range(0, len(bms_list)):
        #if len(bms_list[b]) != 0:
        rfm9x.send(bms_list[b])
        #time.sleep(3)
    #send a packet of length 2 to signal the end of sending
    rfm9x.send(bytes("11", "utf-8"))
    time.sleep(1)
    display.fill(0)
    display.text('Sent packet data!', 25, 15, 1)
    display.show()
    time.sleep(5)
    display.fill(0)
    display.show()
    
    # Step 4: deploy
    print("Deploying profiler")
    display.fill(0)
    display.text('Deploying', 25, 15, 1)
    display.show()
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    t_end = time.time() + depth
    while time.time() < t_end:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
    # stop
    time.sleep(1)
    print("Underwater")
    display.fill(0)
    display.text('Underwater', 25, 15, 1)
    display.show()
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    time.sleep(1)

