#!/usr/bin/env python2
# -*- coding: utf-8 -*-
u"""Capture the screen from the oscilloscope.

The screenshots are saved to captures/ folder with the current datetime
(in ISO format) as the filename.

@author: Tuomo Kohtamäki
"""
import datetime
from scope_functions import DL1540

filename = 'captures/'+datetime.datetime.now().isoformat()+'.tiff'

scope = DL1540(0, 1)
scope.stop()

image_bytearray = scope.screen_capture()
newFile = open(filename, "wb")
newFile.write(image_bytearray)
