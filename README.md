# Scientific Shark

WATER: Wave powered Autonomous Tethered Examining Robot

Repository for the software, CAD, and EAGLE files used/created by the ECE-4873-D1A team Scientific Shark

In 1989, an Exxon oil tanker hit a reef, spilling more than 11 million gallons of oil into Prince William Sound, devastating the ecosystem. A moored profiler was placed in the sound to monitor the health of the ecosystem. Currently, the scientists must go out weekly to charge the profiler and download data. Our project is to design a prototype of a new profiler that includes an innovative way to charge the profiler and communicate the system over longer distances. 

# Video Presentation 

[![Video Presentation](https://img.youtube.com/vi/9g4P57724mM/0.jpg)](https://www.youtube.com/watch?v=9g4P57724mM)

# Code Organization
We have code for three separate systems in this repository
- profiler: contains code running on the Raspberry Pi that is the processing unit for the moored profiler, including running the sending radio, collecting data, and running the winch
- base_station: contains the code running on the base station Raspberry Pi, including the receiving radio and user interface
- diyBMSv4Code @ cd5c401: a submodule containing the diyBMS code created by Stuart Pittaway and modified slightly to send the battery information through the debug pins 

# Installation 

First clone the whole repository:
<code>git clone https://github.com/csmith608/ScientificShark.git </code>

Switch into the ScientificShark directory and initialize the submodule: 

<code>git submodule init</code>

<code>git submodule update</code>

The WEMOS on the diyBMS controller board needs to be flashed with the code in the diyBMSv4Code @ cd5c401 -> ESPController as instructed in this video: https://www.youtube.com/watch?v=wTqDMg_Ql98

Each ATTiny on each diyBMS cell module board also needs to be flash with the code in diyBMSv4Code @ cd5c401 -> ATTINYCellModule as instructed at the end of the above video (https://www.youtube.com/watch?v=wTqDMg_Ql98) 

The Raspberry Pi acting as the profiler will need to be connected as shown in the Pinouts section and the Python file in the profiler directory is run

The Raspberry Pi acting as the base station only has the LoRa Radio bonnet attached and the two Python files in the base_station directory are run

# Libraries

The following python libraries are required:
- PySerial
-- <code>pip3 install pyserial</code>
- matplotlib
-- <code>pip3 install matplotlib</code>
- RPi.GPIO
-- <code>pip3 install RPi.GPIO</code>


To run the python files that include radio sending/receiving the Adafruit CircuitPython libraries must be installed, the directions and wiring are included here https://learn.adafruit.com/adafruit-radio-bonnets/rfm9x-raspberry-pi-setup


For working with the diyBMS code, created by Stuart Pittaway, please see the source repository https://github.com/stuartpittaway/diyBMSv4

Adam Welch has informative videos for working with the diyBMS components: https://www.youtube.com/watch?v=bFUMxgrz-yo 

# Pinouts

![pinout](https://github.com/csmith608/ScientificShark/blob/main/images/Profiler%20pinout.png)

# Licence 

MIT License

Copyright (c) 2020 Scientific Shark

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
