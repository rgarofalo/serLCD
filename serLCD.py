"""
.. module:: serLCD

********
serLCD
********

This module implements the driver for LCD controller SparkFun Serial Enabled LCD Backpack.

It implements most all functions from LiquidCrystal and added a few functions of my own

http://www.sparkfun.com/datasheets/LCD/SerLCD_V2_5.PDF

"""

import streams

class serLCD():

    # LCD Address
    ADDRESS = 0x27

    # commands
    LCD_CLEARDISPLAY =    0x01
    LCD_RETURNHOME =      0x02
    LCD_ENTRYMODESET =    0x04
    LCD_DISPLAYCONTROL =  0x08
    LCD_CURSORSHIFT =     0x10
    LCD_FUNCTIONSET =     0x20
    LCD_SETCGRAMADDR =    0x40
    LCD_SETDDRAMADDR =    0x80
    LCD_SETSPLASHSCREEN = 0x0A
    LCD_SPLASHTOGGLE	= 0x09
    LCD_RETURNHOME =	  0x02

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x4D
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON = 0x0C
    LCD_DISPLAYOFF = 0x08
    LCD_CURSORON = 0x0E
    LCD_CURSOROFF = 0x0C
    LCD_BLINKON = 0x0D
    LCD_BLINKOFF = 0x0C

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x14
    LCD_MOVELEFT = 0x10

    # Flags for setting display size
    LCD_SET2LINE =		0x06
    LCD_SET4LINE =		0x05
    LCD_SET16CHAR =		0x04
    LCD_SET20CHAR =		0x03

    # flags for backlight control
    LCD_BACKLIGHT = 0x80
    LCD_NOBACKLIGHT = 0x00

    new_exception(InvalidNumChars,ValueError,'Invalid number chars! use 16 or 20')
    new_exception(InvalidBacklight,ValueError,'Invalid backlight value! use values range from 1-30. 1=off---30=full')
    new_exception(InvalidRow,ValueError,'Invalid select row, use 0,1,2 or 3')
    new_exception(InvalidColumn,ValueError,'Invalid select column')
    new_exception(InvalidPosition,ValueError,'Invalid position')
    new_exception(InvalidNumLines,ValueError,'Invalid number lines! use: 2 or 4')
    new_exception(InvalidLineOrText,ValueError,'Invalid number line or text(limit chars is 40)')
    new_exception(TextOverflow,ValueError,'Maximum length exceeded (limit chars is 40)')


    """
================
The serLCD class
================

.. class:: serLCD
    Creates a serLCD instance for controlling a diplay with 2 lines and 16 character through a serial port(es. SERIAL1).
    The SerLCD currently supports 16 and 20 character wide screens with 2 or 4 lines of display configurable using the appropriate functions.

    ::
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
    """

    def __init__(self, drivername):
        self._lcd_device = streams.serial(drivername,9600, set_default=False)
        self._numLines = 2
        self._numColumns = 16
        self._lenghTextLine=[0,0,0,0]
        self._textInLine=['','','','']

        self.clear()

    def blinkCursor(self):
        """
.. method:: blinkCursor()
    Turn the blinking cursor on
        """
        self._command(self.LCD_BLINKON)

    def brightness(self, brightness_level):
        """
.. method:: brightness(brightness_level)
    Sets the backlight brightness based on input value. Values range from 1-30. 1=off---30=full brightness
        """
        if brightness_level >= 1 and brightness_level <= 30:
            self._specialCommand(self.LCD_BACKLIGHT | (brightness_level-1))
        else:
            raise InvalidBacklight

        sleep(2)

    def noblinkCursor(self):
        """
.. method::noblinkCursor()
   Turn the blinking cursor off
        """
        self._command(self.LCD_BLINKOFF)

    def clear(self):
        """
.. method:: clear()
    Clear lcd and set to home
        """
        self._command(self.LCD_CLEARDISPLAY)

    def clearLine(self, row):
        """
.. method:: clearLine()
    Clears a single line by writing black spaces then returing cursor to beginning on line.

        """
        if row>=0 and row <= (self._numLines-1):
            p=0
            while p<self._numColumns:
                self.setCursor(row,p)
                self.message(" ")
                p=p + 1

            self.setCursor(row,0)
        else:
            raise InvalidRow

    def cursor(self):
        """
.. method:: cursor()
    Turns the underline cursor on

        """
        self._command(self.LCD_CURSORON)

    def noCursor(self):
        """
.. method:: noCursor()
    Turns the underline cursor off
        """
        self._command(self.LCD_CURSOROFF)

    def setCursor(self, row, col):
        """
.. method:: setCursor(row,col)
    Set cursor to specific row and col (start:0)
        """
        self.row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row <= self._numLines:
            self._command(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))
        else:
            raise InvalidRow

    def display(self):
        """
.. method:: display()
    Turn the display on (quickly)
        """
        self._command(self.LCD_DISPLAYON)

    def noDisplay(self):
        """
.. method:: noDisplay()
    Turn the display off (quickly)
        """
        self._command(self.LCD_DISPLAYOFF)

    def home(self):
        """
.. method:: home()
    Returns cursor to home position
        """
        self._command(self.LCD_RETURNHOME)

    def leftToRight(self):
        """
.. method:: leftToRight()
    This is for text that flows Left to Right
        """
        self._command(self.LCD_ENTRYMODESET | self.LCD_ENTRYLEFT)

    def rightToLeft(self):
        """
.. method:: rightToLeft()
    This is for text that flows Right to Left
        """
        self._command(self.LCD_ENTRYMODESET & (~self.LCD_ENTRYLEFT))

    def message(self, text):
        """
.. method:: message(text)
    Send string to LCD. Newline wraps to second line
        """
        if len(text)<=40:
            for char in text:
                if char == '\n':
                    self._command(0xC0)  # next line
                else:
                    self._write_cmd(ord(char))
        else:
            raise TextOverflow

    def moveCursorRight(self,p):
        """
.. method:: moveCursorRight(position)
    Move cursor right n position
        """
        if p > 0:
            n = 0
            while n < p:
                self._command(self.LCD_MOVERIGHT)
                n = n + 1
        else:
            raise InvalidPosition

    def moveCursorLeft(self,p):
        """
.. method:: moveCursorLeft(position)
    Move cursor left n position
        """
        if p > 0:
            n = 0
            while n < p:
                self._command(self.LCD_MOVELEFT)
                n = n + 1
        else:
            raise InvalidPosition

    def scrollRight(self, position, time=0):
        """
.. method:: scrollRight(position,time=0):
    Scrolls the text on the LCD n positions to the right each time millisecond
        """
        if position > 0:
            n = 0
            while n < position:
                self._command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)
                n=n+1

                if time!=0:
                    sleep(time)
        else:
            raise InvalidPosition

    def scrollLeft(self, position, time=0):
        """
.. method:: scrollLeft(position,time=0)
    Scrolls the text on the LCD n positions to the left each time millisecond
        """
        if position > 0:
            n = 0
            while n < position:
                self._command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)
                n=n+1

                if time!=0:
                    sleep(time)
        else:
            raise InvalidPosition

    def setType(self, lines, chars):
        """
.. method:: setType(lines,chars)
    The SerLCD firmware v2.5 supports setting different types of LCD's. This function allows to easily set the type of LCD.
        """
        if lines==2:
            self._specialCommand(self.LCD_SET2LINE)
            self._numLines=2
        elif lines==4:
            self._specialCommand(self.LCD_SET4LINE)
            self._numLines=4
        else:
            raise InvalidNumLines

        if chars == 16:
            self._specialCommand(self.LCD_SET16CHAR)
            self._numColumns = 16
        elif chars == 20:
            self._specialCommand(self.LCD_SET20CHAR)
            self._numColumns = 20
        else:
            raise InvalidNumChars

    def writeNextLine(self, text):
        """
.. method:: writeNextLine(text):
    Insert the text in new line and moves upwards the text on the LCD
        """
        if len(text)<=40:
            for i in range((self._numLines-1)):
                self.writeLine(i, self._textInLine[i+1])
            self.writeLine(self._numLines-1, text)
            sleep(500)
        else:
            raise TextOverflow


    def writeLine(self, line, text):
        """
.. method:: writeLine(line,text)
    Insert the text in the specification row
        """
        if line<=self._numLines and len(text)<=40:
            self.clearLine(line)
            self.setCursor(line,0)
            self._lenghTextLine[line] = len(text)
            self._textInLine[line] = text

            if len(text) < 16:
                self.message(text)
            else:
                self.message(text[:16])
                sleep(1000)
                for i in range(len(text[16:])):
                    self.scrollLeft(1,0)
                    self.setCursor(line,i+16)
                    self._write_cmd(ord(text[i+16]))
                self.scrollRight(len(text[16:]),0)
        else:
            raise InvalidLineOrText

    def scrollingRightToLeft(self, speed, delay):
        """
.. method:: scrollingRightToLeft(speed, delay):
    Move the text on the LCD from right to left and contrary of n steps if the text exceeds the maximum capacity of line
        """
        while True:
            self.scrollRight(self._lenghTextLine[0]-self._numColumns, speed)
            sleep(delay)
            self.scrollLeft(self._lenghTextLine[0]-self._numColumns, speed)
            sleep(delay)

    def scrollingLeftToRight(self, speed, delay):
        """
.. method:: scrollingLeftToRight(speed, delay):
    Move the text on the LCD from left to right and contrary of n steps if the text exceeds the maximum capacity of line
        """
        while True:
            self.scrollLeft(self._lenghTextLine[0] - self._numColumns, speed)
            sleep(delay)
            self.scrollRight(self._lenghTextLine[0] - self._numColumns, speed)
            sleep(delay)

    def scrolling(self, speed):
        """
.. method:: scrolling(speed)
    Scrolls the text on the LCD a position to the right each time millisecond
        """
        while True:
            self.scrollRight(1, speed)

    def _command(self, value):
        #Private functions for sending the command values
        self._write_cmd(0xFE)
        self._write_cmd(value)
        sleep(5)

    def _specialCommand(self, value):
        #Private functions for sending the special command values
        self._write_cmd(0x7C)
        self._write_cmd(value)
        sleep(5)

    def _write_cmd(self, data):
        print(chr(data),end='',stream=self._lcd_device)
        #self._lcd_device.write(bytes(data));
