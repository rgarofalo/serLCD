.. module:: serLCD

********
serLCD
********

This module implements the driver for LCD controller SparkFun Serial Enabled LCD Backpack.
It implements most all functions from LiquidCrystal and added a few functions of my own http://www.sparkfun.com/datasheets/LCD/SerLCD_V2_5.PDF
    ==================
    The serLCD class
    ==================

.. class:: serLCD(drivername)

    Creates a serLCD instance for controlling a diplay with 2 lines and 16 character through a serial port(es. SERIAL1).
    The SerLCD currently supports 16 and 20 character wide screens with 2 or 4 lines of display configurable using the appropriate functions.

    Example::

        import streams
        import serLCD

        error=streams.serial()
        try:

            lcd=serLCD.lcd(SERIAL1)
            lcd.clear()
            lcd.home()
            lcd.setType(2,16)
            lcd.writeLine(0,'1234567890')

        except Exception as e:
            print(e,stream=error)
     
.. method:: blinkCursor()

    Turn the blinking cursor on
.. method:: brightness(brightness_level)

    Sets the backlight brightness based on input value. Values range from 1-30. 1=off---30=full brightness
.. method: noblinkCursor()

    Turn the blinking cursor off
.. method:: clear()

    Clear lcd and set to home
.. method:: clearLine()

    Clears a single line by writing black spaces then returing cursor to beginning on line.
.. method:: cursor()

    Turns the underline cursor on
.. method:: noCursor()

    Turns the underline cursor off
.. method:: setCursor(row,col)

    Set cursor to specific row and col (start:0)
.. method:: display()

    Turn the display on (quickly)
.. method:: noDisplay()

    Turn the display off (quickly)
.. method:: home()

    Returns cursor to home position
.. method:: leftToRight()

    This is for text that flows Left to Right
.. method:: rightToLeft()

    This is for text that flows Right to Left
.. method:: message(text)

    Send string to LCD. Newline wraps to second line
.. method:: moveCursorRight(position)

    Move cursor right n position
.. method:: moveCursorLeft(position)

    Move cursor left n position
.. method:: scrollRight(position,time=0):

    Scrolls the text on the LCD n positions to the right each time millisecond
.. method:: scrollLeft(position,time=0)

    Scrolls the text on the LCD n positions to the left each time millisecond
.. method:: setType(lines,chars)

    The SerLCD firmware v2.5 supports setting different types of LCD's. This function allows to easily set the type of LCD.
.. method:: writeNextLine(text):

    Insert the text in new line and moves upwards the text on the LCD
.. method:: writeLine(line,text)

    Insert the text in the specification row
.. method:: scrollingRightToLeft(speed, delay):

    Move the text on the LCD from right to left and contrary of n steps if the text exceeds the maximum capacity of line
.. method:: scrollingLeftToRight(speed, delay):

    Move the text on the LCD from left to right and contrary of n steps if the text exceeds the maximum capacity of line
.. method:: scrolling(speed)

    Scrolls the text on the LCD a position to the right each time millisecond
