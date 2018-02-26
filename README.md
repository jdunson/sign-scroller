# sign-scroller
Software to use a LED matrix as a scrolling sign.  

Originally created for use on a Raspberry Pi, with an Adafruit "RGB Matrix HAT + RTC" for Raspberry Pi - Mini Kit (Product ID: 2345), driving a supported number and geometry of HUB75 matrix LED panels.  (Most development and testing up until 2018-02 done on an effective 32 h x 64 w array made from two daisy-chained 32x32 panels.)

https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi
It is suggested that the matrix be set up using the standard instructions provided by Adafruit.  
Originally this included using the Adafruit fork of LED matrix software, on Raspbian 8 (Jessie)

The LED-matrix library is (c) Henner Zeller h.zeller@acm.org with GNU General Public License Version 2.0 http://www.gnu.org/licenses/gpl-2.0.txt
https://github.com/hzeller/rpi-rgb-led-matrix

Compatibility To Do: 
* Test with Raspbian 9 (Stretch)
* Test with the "new" hzeller library (ie, unforked version which is now considered the standard way)
* Test with the new Adafruit "RGB Matrix Bonnet" for Raspberry Pi (Product ID: 3211) hardware


