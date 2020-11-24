import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

fig = plt.figure(figsize=(20,10))
ax1= fig.add_subplot(221)  
ax2 = fig.add_subplot(222)  
ax3 =fig.add_subplot(223)   
ax4 =fig.add_subplot(224)

fig2 = plt.figure(figsize=(20,10))
ax5 =fig2.add_subplot(221)   
ax6 =fig2.add_subplot(222)

listHeading=[]
listRollangle=[]
listPitchangle=[]
listTemp=[]
listCellVolt1=[]
listCellVolt2=[]
listCellVolt3=[]
listCellVolt4=[]
listCellVolt5=[]
listCellVolt6=[]
listCellVolt7=[]
listCellVolt8=[]
listCellTemp1=[]
listCellTemp2=[]
listCellTemp3=[]
listCellTemp4=[]
listCellTemp5=[]
listCellTemp6=[]
listCellTemp7=[]
listCellTemp8=[]

def animateCompass(i):
    pullData = open("compass_info.txt","r").readlines()
    for x in range(0, len(pullData)):
	    firstLine = pullData[x]
	    firstLine = firstLine.replace("'", '')
	    firstLine = firstLine.replace(' ', '')
	    firstLine = firstLine.replace(",", ' ')
	    firstLine = firstLine.replace("[", '')
	    firstLine = firstLine.replace("]", '')
	    firstLine = firstLine.replace("\n", '')
	    firstLine = firstLine.split(' ') #['102.6', '-2.1', '-54.6', '26.3']
	    xs = range(0, len(pullData))
	    print(firstLine)
	    listHeading.append(float(firstLine[0]))
	    listRollangle.append(float(firstLine[1]))
	    listPitchangle.append(float(firstLine[2]))
	    listTemp.append(float(firstLine[3]))
    ax1.clear()
    ax1.plot(xs,listHeading, 'cyan')
    ax2.clear()
    ax2.plot(xs,listRollangle, 'red')
    ax3.clear()
    ax3.plot(xs,listPitchangle, 'purple')
    ax4.clear()
    ax4.plot(xs,listTemp, 'green')
    ax1.set_title('Heading vs reading')
    ax1.set_xlabel('reading')
    ax1.set_ylabel('Heading')
    ax2.set_title('Rollangle vs reading')
    ax2.set_xlabel('reading')
    ax2.set_ylabel('Rollangle')
    ax3.set_title('Pitchangle vs reading')
    ax3.set_xlabel('reading')
    ax3.set_ylabel('Pitchangle')
    ax4.set_title('Temperature vs reading')
    ax4.set_xlabel('reading')
    ax4.set_ylabel('Temperature')
    listHeading.clear()
    listRollangle.clear()
    listPitchangle.clear()
    listTemp.clear()

def animateBms(i):
    with open("/home/pi/Desktop/diybms_temperature.txt", "r") as f: #reading cell data
        celldatatemp = f.readlines()# ten lines 
        print(celldatatemp)
    
    for yy in range(0,len(celldatatemp)):
        tempLine = celldatatemp[yy]
        tempLine = tempLine.replace("'", '')
        #Line = Line.replace(' ', '')
        tempLine = tempLine.replace(",", ' ')# 3.73 0.0 0.0 0.0 0.0 0.0 0.0 0.0 
        tempLine = tempLine.replace("[", '')
        tempLine = tempLine.replace("]", '')
        tempLine = tempLine.replace("\n", '')
        tempLine = tempLine.split(' ')
        print(tempLine[0])
        cellnumtemp = range(0, len(celldatatemp))
        listCellTemp1.append(float(tempLine[0]))
        listCellTemp2.append(float(tempLine[1]))
        listCellTemp3.append(float(tempLine[2]))
        listCellTemp4.append(float(tempLine[3]))
        listCellTemp5.append(float(tempLine[4]))
        listCellTemp6.append(float(tempLine[5]))
        listCellTemp7.append(float(tempLine[6]))
        listCellTemp8.append(float(tempLine[7]))
	
    with open("/home/pi/Desktop/diybms_voltage.txt", "r") as f: #reading cell data
        celldata = f.readlines()# ten lines 

    while(len(celldata) < 2):
        with open("/home/pi/Desktop/diybms_voltage.txt", "r") as f:
            celldata = f.readlines()# read lines from the file 
        print("Waiting for enough data to be be present")

    for xx in range(0,len(celldata)-1):
        Line = celldata[xx]
        Line = Line.replace("'", '')
        #Line = Line.replace(' ', '')
        Line = Line.replace(",", ' ')# 3.73 0.0 0.0 0.0 0.0 0.0 0.0 0.0 
        Line = Line.replace("[", '')
        Line = Line.replace("]", '')
        Line = Line.replace("\n", '')
        Line = Line.split(' ')
        print(Line[0])
        cellnum = range(1, len(celldata))
        listCellVolt1.append(float(Line[0]))
        listCellVolt2.append(float(Line[1]))
        listCellVolt3.append(float(Line[2]))
        listCellVolt4.append(float(Line[3]))
        listCellVolt5.append(float(Line[4]))
        listCellVolt6.append(float(Line[5]))
        listCellVolt7.append(float(Line[6]))
        listCellVolt8.append(float(Line[7]))
    ax5.clear()
    ax5.plot(cellnumtemp,listCellTemp1, 'red')
    ax5.plot(cellnumtemp,listCellTemp2, 'orange')
    ax5.plot(cellnumtemp,listCellTemp3, 'yellow')
    ax5.plot(cellnumtemp,listCellTemp4, 'green')
    ax5.plot(cellnumtemp,listCellTemp5, 'blue')
    ax5.plot(cellnumtemp,listCellTemp6, 'cyan')
    ax5.plot(cellnumtemp,listCellTemp7, 'm')
    ax5.plot(cellnumtemp,listCellTemp8, 'k')
    ax6.clear()
    ax6.plot(cellnum,listCellVolt1, 'red')
    ax6.plot(cellnum,listCellVolt2, 'orange')
    ax6.plot(cellnum,listCellVolt3, 'yellow')
    ax6.plot(cellnum,listCellVolt4, 'green')
    ax6.plot(cellnum,listCellVolt5, 'blue')
    ax6.plot(cellnum,listCellVolt6, 'cyan')
    ax6.plot(cellnum,listCellVolt7, 'm')
    ax6.plot(cellnum,listCellVolt8, 'k')
    ax5.set_title('Temperature vs reading')
    ax5.set_xlabel('reading')
    ax5.set_ylabel('Temp (degrees C)')
    ax6.set_title('Voltage vs reading')
    ax6.set_xlabel('reading')
    ax6.set_ylabel('Voltage (V)')
    listCellTemp1.clear()
    listCellTemp2.clear()
    listCellTemp3.clear()
    listCellTemp4.clear()
    listCellTemp5.clear()
    listCellTemp6.clear()
    listCellTemp7.clear()
    listCellTemp8.clear()
	
ani = animation.FuncAnimation(fig, animateCompass, interval=1000)
aniBms = animation.FuncAnimation(fig2, animateBms, interval=1000)
plt.show()
