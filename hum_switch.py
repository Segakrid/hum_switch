#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from time import sleep, strftime
import Adafruit_DHT
import RPi.GPIO as GPIO


GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)

sensor = Adafruit_DHT.DHT22
pin = 4
fan_status = "uit"

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!

# while True: # uncomment when sleep is set to 60 sec
for i in range(5):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
        if humidity >= 50 and fan_status == "uit":
            GPIO.output(23, True)
            fan_status = "aan"
            print 'De ventilator is nu {0}'.format(fan_status)
        elif humidity >= 50 and fan_status == "aan":
            print "De ventilator blijft {0}".format(fan_status)
        elif humidity < 50 and fan_status == "aan":
            GPIO.output(23, False)
            fan_status = "uit"
            print "De ventilator is nu {0}".format(fan_status)
        elif humidity < 50 and fan_status == "uit":
            print "De ventilator blijft {0}".format(fan_status)

        if strftime("%M") in ["00", "10", "20", "30", "40", "50"]:
            with open('~/log/hum_bathroom.txt', 'w') as fp:
                fp.write("{0}: {1}".format(strftime("%D %T"), humidity, temperature))
    else:
        print 'Failed to get reading. Try again!'
        sys.exit(1)
    sleep(3)

