# Route-advisor steering for Euro Truck Simulator 2

## Overview

This script, written in Python, continuously scans a specific region of pixels
of the in-game route advisor overlay window. The route to be followed is
presented in-game by a red line and the script looks for these red pixels to
determine an *error value* and then calculates the amount of steering that is
needed.

Because it is driven by red pixels on-screen, it will struggle to keep on the
center of the road when the red guidance line is disturbed, for example when the
current road crosses over a later or earlier section of the route or when the
route advisor tells you to shift lanes. At that point, it becomes unreliable, so
it is advised to set up some sort of keyboard shortcut or similar to suspend the
script and take over manual control.

## Setup

The setup is pretty straight-forward. The script is written in Python and
requires the dependencies NumPy, mss and pynput. When Python is installed, you
can install the dependencies using:

```sh
pip install numpy mss pynput
```

To download a copy of the script, clone the repository from GitHub (if you know
how to use Git) or manually download from
[here](https://raw.githubusercontent.com/quicoa/ets2_ras/master/ras.py).

You can then launch the script however you like, for example, to run from your
shell in the directory where you downloaded the script, type:

```sh
python3 ./ras.py
```

Newer versions of python may complain about not running inside a virtual
environment. To set up a virtual environment, execute the commands it advises
you to run, which should be something like:

```sh
python3 -m venv --system-site-packages .
```

You can now install the dependencies in this virtual environment and run the
script:

```sh
./bin/python3 -m pip install numpy mss pynput
./bin/python3 ./ras.py
```

When no errors occur, the script is running and scanning your screen. Before
entering the road, take a moment to tweak and verify pre-defined parameters in
the script to make sure it won't get confused and unintentionally damage your
truck.

## Tweaking

Before taking your truck for a joyride, please take a look at the configuration
values defined inside the script. The most important one being the position of
the route advisor on your screen and the extracted region of interest. Take a
screenshot of your game and open the image in an image editor of your choice.
If you don't have a preference, GIMP (https://www.gimp.org) is free and
open-source. In the image editor, you can check the coordinates of each pixel.
Verify that the positions in your screenshot match with the parameters defined
in the script and if not, adjust them accordingly.

## Driving

Time to drive! Open Euro Truck Simulator 2 and enable steering with the mouse.
For now, only mouse controls are supported. Keyboard steering may be added in
the future.

Go to a relatively silent area or road and drive at a low speed to prevent
damaging your truck in case something goes wrong. Make sure the script is
running and that your route advisor is on the most zoomed-in view. When it
detects red pixels, it will engage and start steering.

## Be cautious

This is nowhere close to a 'set and forget' setup, you as a truck driver remain
all responsibility for your own safety and anyone else on the road. The software
monitors the navigation display and does not take any road features, obstacles
or traffic into account. You'll need to take back manual control of the vehicle
regularly, as this is only an assistant. Please keep this in mind.

