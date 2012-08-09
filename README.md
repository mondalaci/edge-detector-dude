Edge Detector Dude
==================

Edge Detector Dude is a sweet and sexy graphics utility as can be
seen on the following screenshot:

![](/mondalaci/edge-detector-dude/raw/master/screenshot.png)

It computes and renders the Sobel edge-detected and
the gradient-directed versions of the input image.  The pixels of the
gradient-directed image are computed by denoting the angle of the
gradients of the pixels and mapping their value to the relevant
grayscale colors.

Edge Detector Dude is actually a front end that uses the accompanying
gradient utility that processes the input image.  Edge Detector Dude
is written in Python using the PyGTK GUI library.  gradient is written
in C using the Allegro game programming library.

I put together this bad boy in 2005 as a university project and don't
plan to touch it again.  Also, I think I screwed the algorithm for the
gradient-directed image because it doesn't resemble anything
recognizable.  Oh well...

Build
-----

To build gradient, you'll need the Allegro developer library which
is contained by the `liballegro-dev` package on Debian.  After having
the dependencies installed you can easily build gradient by invoking
make.

You don't have to build Edge Detector Dude, since it's a Python
application however you'll need to have the PyGTK and the Python Glade
packages installed which are named as `python-gtk2` and `python-glade2`
in Debian.

Install
-------

Copy the package directory to any place you want.  After that modify
the program_dir variable in the beginning of the edge-detector-dude.py
file to reflect the actual pathname of the application.

You can invoke Edge Detector Dude from any place from this moment on.
