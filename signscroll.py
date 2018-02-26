#!/usr/bin/python

# Originally based on Adafruit example code
# Gradually improved and substantially added to over several versions by James R. Dunson (jdunson, JRD)
# It turns out that this is calling an old and now depreciated Adafruit fork of the hzeller code
#     (this was the recommended setup when the hardware was purchased several years ago)

# Major version history
# ada-matrix.py : 2016-03-01
# matrixdemo.py : 2016-06-17
# pngscroll2-vtsffcrand.py : 2016-09-01
# pngscroll2-vtsffcrand[2,3].py : 2017-09-08
# signscroll4.py : 2018-02-23
# signscroll4[b,c].py : 2018-02-25

### Original Adafruit comments
# A more complex RGBMatrix example works with the Python Imaging Library,
# demonstrating a few graphics primitives and image loading.
# Note that PIL graphics do not have an immediate effect on the display --
# image is drawn into a separate buffer, which is then copied to the matrix
# using the SetImage() function (see examples below).
# Requires rgbmatrix.so present in the same directory.

# PIL Image module (create or load images) is explained here:
# http://effbot.org/imagingbook/image.htm
# PIL ImageDraw module (draw shapes to images) explained here:
# http://effbot.org/imagingbook/imagedraw.htm

# Import section

import Image
import ImageDraw
import time
from rgbmatrix import Adafruit_RGBmatrix
import random
import os
import glob
import sys


# command line parsing, very primitive
if len(sys.argv) > 1:
    orgbase = sys.argv[1]
else:
    orgbase = ''
    if verbosity > 0:
        print "Fatal Error: No orgbase specified on command line, exiting"
    sys.exit(2)     # In this version, we fail if no orgbase specified

if len(sys.argv) > 2:
    verbosity = int(sys.argv[2])
else:
    verbosity = 1       # 0 is silent, 1 is normal, 2 is some debug output
    
# User-settable variables and configuration
staticslide = orgbase + '-static.png'
if verbosity > 1:
    print staticslide
scrollwidth = '128'     # only tested in cases where greater than dispwidth
scrollsearch = orgbase + '-' + scrollwidth + '*png'
scrollpngs = glob.glob(scrollsearch)
if verbosity > 1:
    print scrollpngs
numscrolls = len(scrollpngs)
if verbosity > 1:
    print numscrolls
if numscrolls < 1:
    if verbosity > 0:
        print "Fatal Error: No scrolling PNGs found, exiting"
    sys.exit(2)
slidesearch = orgbase + '-slide*png'
slidepngs = glob.glob(slidesearch)
if verbosity > 1:
    print slidepngs
numslides = len(slidepngs)
if verbosity > 1:
    print numslides
if numslides < 1:
    if verbosity > 0:
        print "Warning: No slide PNGs found, using static"
    slidepngs = [staticslide]
    numslides = 1
    
# delays, in decimal seconds, to hold the relevant display
scrollwait = 0.025
slidewait = 3.0
staticwait = 3.0
# Note: the width of the matrix is assumed by underlying code to be 32.  
# This is not good as 64x64 panels are now available
matrixcols = 32     # 32, the pixel width of a matrix; do not change from 32, will break things
matrixrows = 32     # 32 or 16, the pixel height of a matrix; not well tested with anything other than 32
nummatrix = 2       # the number of chained matrix; not well tested with anything other than 2
dispheight = matrixcols
dispwidth = matrixrows * nummatrix
if verbosity > 1:
    print str(dispheight) + " h x " + str(dispwidth) + " w"

# Rows and chain length are both required parameters:
# Note: this normally prints a Result line that is somewhat undesirable, several experiments to suppress didn't work

matrix = Adafruit_RGBmatrix(matrixrows, nummatrix)

### This is stuff from the original Adafruit example that is not currently set up
### begin dead code block

# Bitmap example w/graphics prims
#image = Image.new("1", (32, 32)) # Can be larger than matrix if wanted!!
#draw  = ImageDraw.Draw(image)    # Declare Draw instance before prims
# Draw some shapes into image (no immediate effect on matrix)...
#draw.rectangle((0, 0, 31, 31), fill=0, outline=1)
#draw.line((0, 0, 31, 31), fill=1)
#draw.line((0, 31, 31, 0), fill=1)
# Then scroll image across matrix...
#for n in range(-32, 33): # Start off top-left, move off bottom-right
#	matrix.Clear()
#	IMPORTANT: *MUST* pass image ID, *NOT* image object!
#	matrix.SetImage(image.im.id, n, n)
#	time.sleep(0.05)

# 8-bit paletted GIF scrolling example
#image = Image.open("cloud.gif")
#image.load()          # Must do this before SetImage() calls
#matrix.Fill(0x6F85FF) # Fill screen to sky color
#for n in range(32, -image.size[0], -1): # Scroll R to L
#	matrix.SetImage(image.im.id, n, 0)
#	time.sleep(0.025)

# 24-bit RGB scrolling example.
# The adafruit.png image has a couple columns of black pixels at
# the right edge, so erasing after the scrolled image isn't necessary.

### end dead code block

# "memory" variable init, do not adjust

oldimage2 = ''
oldimage1 = ''
newimage = ''
oldslide2 = ''
oldslide1 = ''
newslide = ''

def showscroll():
    # pick a random scrolling image to scroll
    # if there are 3 or fewer images they will alternate predictably
    global oldimage2, oldimage1, newimage
    matrix.Clear()
    if numscrolls > 2:
        oldimage2 = oldimage1
    else:
        oldimage2 = ''
    if numscrolls > 1:
        oldimage1 = newimage
    else:
        oldimage1 = ''
    newimage = random.choice(scrollpngs)
    while (newimage == oldimage1) or (newimage == oldimage2):
        newimage = random.choice(scrollpngs)
    image = Image.open(newimage)
    image.load()
    for n in range(32, -image.size[0], -1):
        matrix.SetImage(image.im.id, n, 1)
        time.sleep(scrollwait)
    return;

def showstatic():    
    # show the static slide
    matrix.Clear()
    image = Image.open(staticslide)
    image.load()
    matrix.SetImage(image.im.id, 0, 1)
    time.sleep(staticwait)
    return;

def showslide():
    # pick a random variable slide to show
    # if there are 3 or fewer slides they will alternate predictably
    global oldslide2, oldslide1, newslide
    matrix.Clear()     
    if numslides > 2:
        oldslide2 = oldslide1
    else:
        oldslide2 = ''
    if numslides > 1:
        oldslide1 = newslide
    else:
        oldslide1 = ''
    newslide = random.choice(slidepngs)
    while (newslide == oldslide1) or (newslide == oldslide2):
        newslide = random.choice(slidepngs)
    image = Image.open(newslide)
    image.load()
    matrix.SetImage(image.im.id, 0, 1)   
    time.sleep(slidewait)
    return;

# Main block
if verbosity > 0: 
    print('CTRL-C to break loop')
    
try:
    while 1:
        # pick a random scrolling image to scroll
        showscroll()
        
        # show the static slide
        showstatic()
        
        # pick a random scrolling image to scroll (again)
        showscroll()
        
        # pick a random variable slide to show
        showslide()
        
except KeyboardInterrupt:
    pass
matrix.Clear()
