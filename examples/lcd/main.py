################################################################################
# lcd
#
# Created: 2016-04-06 14:35:49.885160
#
################################################################################

import streams
import serLCD

error=streams.serial()
try:

    lcd=serLCD.serLCD(SERIAL1)
    lcd.clear()
    lcd.home()

    lcd.writeLine(0,'Hello World!!')
    lcd.writeLine(1,'Zerynth Team')

    thread(lcd.scrollingLeftToRight(1000,1000))

    print('ok1',end='',stream=error)
except Exception as e:
    print(e,stream=error)

