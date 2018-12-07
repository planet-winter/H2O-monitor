#!/usr/bin/env python3


__author__ = 'Daniel Winter'


try:
    import RPi.GPIO as GPIO
    rpi = True
except:
    rpi = False
    print('RPi.GPIO not installed')

import asyncio
import datetime

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Numeric, MetaData, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TypeDecorator
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from pytz import timezone
from datetime import datetime


bounce = 100

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

pulse_pins = []
pulse_pins.append(source1_pulse_pin)
pulse_pins.append(source2_pulse_pin)
pulse_pins.append(source3_pulse_pin)
pulse_pins.append(source4_pulse_pin)
pulse_pins.append(source5_pulse_pin)
pulse_pins.append(source6_pulse_pin)
pulse_pins.append(source7_pulse_pin)
pulse_pins.append(source8_pulse_pin)
pulse_pins.append(source9_pulse_pin)
pulse_pins.append(source10_pulse_pin)
pulse_pins.append(source11_pulse_pin)
pulse_pins.append(source12_pulse_pin)

# initialize  pulse counter
pulses = [0] * len(pulse_pins)


db_string = "postgres://h2o:h2o@localhost/h2o"

metadata = MetaData()



def time_now():
    UTC = timezone('UTC')
    return datetime.now(UTC)


h2o_logentry = Table('h2olog', metadata,
                   Column('id',Integer(), primary_key=True, autoincrement=True),
                   Column('timestamp', TIMESTAMP(timezone=True), primary_key=False, nullable=False, default=time_now),
                   Column('source1', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source2', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source3', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source4', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source5', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source6', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source7', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source8', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source9', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source10', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source11', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False)),
                   Column('source12', Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=False))
)


global db
db = create_engine(db_string)
metadata.create_all(db)



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

    await log_h2oflow()

    reset_pulses()



async def log_h2oflow():

    global pulses
    logline = h2o_logentry.insert().values(
                                     source1=pulses[0],
                                     source2=pulses[1],
                                     source3=pulses[2],
                                     source4=pulses[3],
                                     source5=pulses[4],
                                     source6=pulses[5],
                                     source7=pulses[6],
                                     source8=pulses[7],
                                     source9=pulses[8],
    )
    global db
    conn = db.connect()
    result = conn.execute(logline) # no clue how to use ORM and async...
    conn.close()



def countpulse_callback(channel):
    global pulses
    pin = pulse_pins.index(channel)
    pulses[pin] += 1


def reset_pulses():
    global pulses
    global pulse_pins
    pulses = [0] * len(pulse_pins)



async def main():

    global db
    db = create_engine(db_string)

    if rpi:
        GPIO.setmode(GPIO.BOARD)

        for pin in pulse_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=countpulse_callback, bouncetime=bounce)

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


