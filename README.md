Edge Detector Dude
==================

Edge Detector Dude is a sweet and sexy graphics utility as can be
seen on the following screenshot:

![](edge-detector-dude/raw/master/screenshot.png)

It computes and renders the Sobel edge-detected and
the gradient-directed versions of the input image.  The pixels of the
gradient-directed image are computed by denoting the angle of the
gradient of the pixels and mapping their value as a grayscale color.

Edge Detector Dude is actually a front end that uses the accompanying
gradient utility that processes the input image.

Edge Detector Dude is written in Python using PyGTK GUI library.
gradient is written in C using the Allegro game programming library.

I put together this bad boy in 2005 as a university project and don't
plan to touch it again.  Also, I think I screwed the algorithm of the
gradient-directed image because it doesn't resemble anything
recognizable.  Oh well...