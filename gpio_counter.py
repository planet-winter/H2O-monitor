#!/usr/bin/env python3

__author__ = 'Daniel Winter'


try:
    import RPi.GPIO as GPIO
    rpi = True
except:
    rpi = False
    print('RPi.GPIO not installed')

import asyncio


bounce = 1

# pin = channel
pulse_pin1 = 7
pulse_pin2 = 11
pulse_pin3 = 13
pulse_pin4 = 15
pulse_pin5 = 29
pulse_pin6 = 31
pulse_pin7 = 33
pulse_pin8 = 35
pulse_pin9 = 37


pulse_pins = []
pulse_pins.append(pulse_pin1)
pulse_pins.append(pulse_pin2)
pulse_pins.append(pulse_pin3)
pulse_pins.append(pulse_pin4)
pulse_pins.append(pulse_pin5)
pulse_pins.append(pulse_pin6)
pulse_pins.append(pulse_pin7)
pulse_pins.append(pulse_pin8)
pulse_pins.append(pulse_pin9)

# initialize  pulse counter
pulses = [0] * len(pulse_pins)




def reset_pulses():
    global pulses
    global pulse_pins
    pulses = [0] * len(pulse_pins)


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while True:
            await asyncio.sleep(self._timeout)
            await self._callback()


    def cancel(self):
        self._task.cancel()




async def pulsecounter_timer_callback():
    await asyncio.sleep(0.1)
    global pulses
    print("pulses:", pulses)
    reset_pulses()



def eventHandlerPulsePin1(channel):
    countpulse(1,GPIO.input(channel))

def eventHandlerPulsePin2(channel):
    countpulse(2,GPIO.input(channel))

def eventHandlerPulsePin3(channel):
    countpulse(3,GPIO.input(channel))

def eventHandlerPulsePin4(channel):
    countpulse(4,GPIO.input(channel))

def eventHandlerPulsePin5(channel):
    countpulse(5,GPIO.input(channel))

def eventHandlerPulsePin6(channel):
    countpulse(6,GPIO.input(channel))

def eventHandlerPulsePin7(channel):
    countpulse(7,GPIO.input(channel))

def eventHandlerPulsePin8(channel):
    countpulse(8,GPIO.input(channel))

def eventHandlerPulsePin9(channel):
    countpulse(9,GPIO.input(channel))


def countpulse(channel):
    global pulses
    pin = pulse_pins.index(channel)
    pulses[pin] += 1



async def main():

    if rpi:
        GPIO.setmode(GPIO.BOARD)

        for pin in pulse_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=countpulse, bouncetime=bounce)

        timer = Timer(1, pulsecounter_timer_callback)


    while True:  # CTRL+C to break - requires graceful exit
        try:
            if rpi:
                # continue
                await asyncio.sleep(0.1)
            else:
                pass
                #countpulse()
        except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit






loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


