#!/bin/python3
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2023 Quico Augustijn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Route advisor steering for Euro Truck Simulator 2
#
# Monitor the red line of the in-game route advisor and steer with the mouse
# controls to keep the truck on road.

import time
import numpy as np
from mss import mss
from pynput import mouse

# Region of interest (roi) of the screen
#
# Preferably, half the 'width' parameter and the 'left' parameter added together
# should be the center position of the blue triangle on the route advisor and
# this should also be the center of your region of interest.
# A higher 'width' will give a greater field-of-view, but will be less
# performant.
# The defaults were determined when the game was in fullscreen.
roi = {"top": 848, "left": 1584, "width": 210, "height": 1}

# Horizontal position of the center of the road (blue triangle on the route
# advisor)
#
# This should be the center of the region of interest.  If you have changed the
# region of interest parameters so that this is not the case, set the position
# here manually.
center_static = roi["width"] / 2 - 0.5
#center_static = 104.5

# Sensitivity:
# How much the software should respond to the error value.  This will cause
# steering when the error is significant (that is, we are not driving where we
# should)
sensitivity = float(1 / 4)

# Responsiveness:
# How much the software should respond to a change in error value.  This will
# cause steering when the error is changing during multiple iterations (that's
# usually when we're in a turn)
responsiveness = float(15)

# Iteration speed:
# How fast the software should iterate and adjust the steering controls.  A
# higher number means shorter iteration sleep time.
iteration_speed = 50

# Color range
#
# Color values used to determine whether a pixel is colored or not.  You can
# adjust these colors to you liking, but the default reddish color should be
# fine.  Colors range from 0 to 255
red_min = 200
red_max = 255
green_min = 0
green_max = 25
blue_min = 0
blue_max = 25

# Function that decides if a pixel is colored
def is_pixel_colored(red, green, blue):
    return red >= red_min and red <= red_max and \
           green >= green_min and green <= green_max and \
           blue >= blue_min and blue <= blue_max

# Grab an instance of mss (for taking screenshots)
sct = mss()

# Grab an instance of the mouse controls
mouse = mouse.Controller()

# Variable containing the recorded error value from the previous iteration
old_error = None

# Run for as long as we're allowed to live
while(True):
    # Grab the region of interest of the screen
    screen = sct.grab(roi)
    img = np.array(screen)

    # The image should be only one row in height
    row = img[0]

    # Get the length (amount of pixels horizontally)
    length = len(img[0])

    # Set the initial pixel information
    first_pixel = length # First colored pixel
    last_pixel = 0 # Last colored pixel
    found_first = False # If the first colored pixel is found
    found_last = False # If the last colored pixel is found

    # Iterate over each pixel in the row
    for x in range(length):
        # Current pixel
        pixel = row[x];

        # Get each RGB value of this pixel
        red = pixel[2]
        green = pixel[1]
        blue = pixel[0]

        # Only save this position if it is the very first colored pixel
        if x < first_pixel and is_pixel_colored(red, green, blue):
            first_pixel = x
            found_first = True

        # Only save this position if it is the very last colored pixel
        if x > last_pixel and is_pixel_colored(red, green, blue):
            last_pixel = x
            found_last = True

    # Only respond when colored pixels were found
    if found_first and found_last:
        # Calculate the center of the colored area
        center_position = float(last_pixel - first_pixel) / 2

        # Calculate the error value
        error = float(first_pixel + center_position - center_static)

        # Do not respond on first iteration (change in error is not known yet)
        if old_error != None:
            # Calculate the difference in error compared to the previous iteration
            move = (error - old_error) * responsiveness

            # Also take the error into account
            move += error * sensitivity

            # Now move the mouse
            mouse.move(move, 0) # change in y is 0

        # Record the current error for the next iteration
        old_error = error

    # Give our actions a little time to take effect
    time.sleep(1 / iteration_speed)
