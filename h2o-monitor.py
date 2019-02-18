#!/usr/bin/env python3


__author__ = 'Daniel Winter'


try:
    import RPi.GPIO as GPIO
    rpi = True
except:
    rpi = False
    print('RPi.GPIO not installed')
from influxdb import InfluxDBClient
from datetime import datetime
import time
from pytz import timezone
import sys


LITERS_PER_PULSE = 1
BOUNCETIME = 2

# pin = channel
source1_pulse_pin = 7
source2_pulse_pin = 11
source3_pulse_pin = 13
source4_pulse_pin = 15
source5_pulse_pin = 29
source6_pulse_pin = 31
source7_pulse_pin = 33
source8_pulse_pin = 35
source9_pulse_pin = 37
source10_pulse_pin = 12
source11_pulse_pin = 16
source12_pulse_pin = 18

PULSE_PINS = []
PULSE_PINS.append(source1_pulse_pin)
PULSE_PINS.append(source2_pulse_pin)
PULSE_PINS.append(source3_pulse_pin)
PULSE_PINS.append(source4_pulse_pin)
PULSE_PINS.append(source5_pulse_pin)
PULSE_PINS.append(source6_pulse_pin)
PULSE_PINS.append(source7_pulse_pin)
PULSE_PINS.append(source8_pulse_pin)
PULSE_PINS.append(source9_pulse_pin)
PULSE_PINS.append(source10_pulse_pin)
PULSE_PINS.append(source11_pulse_pin)
PULSE_PINS.append(source12_pulse_pin)



client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('h2o')



json_data = []
write_counter = 0


def time_now():
    UTC = timezone('UTC')
    return datetime.now(UTC)



def pulse_2_liters(pulses):
    return pulses * LITERS_PER_PULSE



def channel_2_source(channel):
    return PULSE_PINS.index(channel)



def log_pulse(channel):

    global json_data
    global write_counter

    new_json_data = {
	"measurement": "h2oflow",
       	"tags": {
        	"source": channel_2_source(channel),
        },
        "time": time_now(),
        "fields": {
        	"liters": pulse_2_liters(1), 
      	}
    }

    json_data.append(new_json_data)
    write_counter+=1
    # batch n writes together
    if write_counter == 100:
        client.write_points(json_data)
        write_counter = 0
        json_data = []


def main():

    if rpi:
        GPIO.setmode(GPIO.BOARD)
        for pin in PULSE_PINS:
            print("setting up pin", pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=log_pulse, bouncetime=BOUNCETIME)
    else:
        print("This code only runs on a Raspberry Pi")

    while True:
        try:
            pass
            #time.sleep(float(BOUNCETIME/1000))
        except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
            sys.exit(1)

if __name__== "__main__":
  main()
