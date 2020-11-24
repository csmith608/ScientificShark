# Import Python System Libraries
import time
from bs4 import BeautifulSoup
import re
import sys
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

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

class Compass():
    heading = 0
    pitchAngle = 0
    rollAngle = 0
    temperature = 0

compassList = []
bmsList = []
voltage = []
temperature = []
List = []

bmsFlag = False
packetDone = False

while True:
    
    packet = None
    # draw a box to clear the image
    # check for packet rx
    # can only receive 252 byte packets at a time
    packet = rfm9x.receive()
    if packet is not None:
        print("Received: ", packet)
        display.fill(0)
        display.text('- received-', 15, 20, 1)
        display.show()
        if(len(packet) == 1):
            bmsFlag = True
        elif(len(packet) == 2):
            packetDone = True
            bmsFlag = False
        # if flag is not set then build the compass packet
        elif bmsFlag:
            bmsList.append(packet)
        else:
            compassList.append(packet)
    
    
    if packetDone:
        for c in range(0, len(compassList)):
            print("compass list: ", compassList[c])
        for b in range(0, len(bmsList)):
            print("diyBMS list:", bmsList[b])
        #reset packet done
        packetDone = False
        
        
        for c in range(len(compassList)):
            
            line = compassList[c].decode('utf-8').rstrip()
            '''
            step_0 = line.split("C")
            step_1 = step_0[1].split("P")
            compass.heading = step_1[0]
            List.append(compass.heading)
            List.append(compass.heading)
            
            str1 = ""
            str1 = str1.join(line)
            '''
            compass = Compass()
            compass.heading = line[line.find('$C')+len('$C'):line.rfind('P')]
            List.append(compass.heading)
            compass.pitchAngle = line[line.find('P')+len('P'):line.rfind('R')]
            List.append(compass.pitchAngle)
            compass.rollAngle = line[line.find('R')+len('R'):line.rfind('T')]
            List.append(compass.rollAngle)
            compass.temperature = line[line.find('T')+len('T'):line.rfind('*')]
            List.append(compass.temperature)
            # sending this data from one radio to other radio
            
            with open("compass_info.txt","a+") as f: #in write mode
                f.write("{}\n".format(List))
            f.close()
            List.clear()
        #parse diyBMS information 
        for x in range(len(bmsList)):
            step_0 = bmsList[x].decode('utf-8').split(':')
            if(step_0[0] == "R"):
                step_1 = step_0[1]
                step_2 = step_1.split("/")
                if(step_2[1] == "83"):
                    step_3 = step_2[2]
                    step_4 = step_3.split("=")
                    #first item is sequence number
                    #second is data separated by spaces
                    temp = step_4[1].split(" ")
                    for t in range(16):
                        if t % 2 == 0:
                            if(temp[t] != '0' and temp != '' and temp != ' '):
                                temperature.append(int(temp[t], 16)/256 - 40)
                            elif(temp[t] != ''):
                                temperature.append(int(temp[t], 16))   
                    with open("diybms_temperature.txt", "a") as f :
                        for i in range(len(temperature)):
                            f.write(str(temperature[i]))
                            f.write(" ")
                        f.write("\n")
                    temperature.clear()
                    f.close
                    #temp = temp[0]
                    #turn temperature from str to int and from hex to decimal
                    #temperature.append(int(temp, 16) - 40)
                    #print(temp)
                    print("Cmd: 83")
                elif(step_2[1] == "81"):
                    step_3 = step_2[2]
                    step_4 = step_3.split("=")
                    #first item is sequence number
                    #second is data separated by spaces
                    volt = step_4[1].split(" ")
                    for t in range(len(volt)):
                        if t % 2 == 0 and volt[t] != 0 and volt[t] != '':
                            voltage.append(int(volt[t], 16)/1000)
                    with open("diybms_voltage.txt", "a") as f :
                        for i in range(len(voltage)):
                            f.write(str(voltage[i]))
                            f.write(" ")
                        f.write("\n")
                    voltage.clear()
                    f.close
                    print("Cmd: 81")
        bmsList.clear
        compassList.clear
        List.clear

        

